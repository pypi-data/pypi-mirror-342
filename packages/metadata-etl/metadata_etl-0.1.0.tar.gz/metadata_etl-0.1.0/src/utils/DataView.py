import json
import h5py
from pathlib import Path


def visitor_func(name, node):
    if isinstance(node, h5py.Dataset):
        print(f"{name} is a dataset")
    else:
        print(f"{name} is a group")


class H5DataIndex:
    def __init__(self, prefix="CONTROL"):
        # Store an empty list for dataset names
        self.names = []
        self.groups = []
        self.files = []
        self.prefix = prefix
        self.data = {prefix: {}}

    def __call__(self, name, h5obj):
        # only h5py datasets have dtype attribute, so we can search on this
        # if hasattr(h5obj,'dtype') and not name in self.names:
        if isinstance(h5obj, h5py.Dataset):
            self.names += [name]
            self.insert_path(name, {"file": len(self.files) - 1, "key": name})
        else:
            # node is a group
            # print(f"{name} is a group")
            self.groups += [name]
            pass

    def insert_path(self, name, metadata):
        parent = self.data
        key = self.prefix
        cursor = parent.get(key, {})
        for p in name.split('/')[:-1]:
            if p in {'MDL'}:
                continue
            # if p in {'value', 'timestamp'}:
                # parent[key] = 0
                # continue
            if p not in cursor:
                cursor[p] = {}

            parent = cursor
            key = p
            cursor = parent.get(key, {})
        parent[key] = metadata

    def get_metadata(self, name):
        parent = self.data
        key = self.prefix
        cursor = parent.get(key, {})
        for p in name.split('/')[1:]:
            if p in {'MDL'}:
                continue
            if p not in cursor:
                return {"error": f"Path does not exist, starting from {p}"}
            parent = cursor
            key = p
            cursor = parent.get(key)
        return cursor | {"file": str(self.files[cursor.get("file")])}

    def register_file(self, filename):
        self.files += {filename}


class H5JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, H5DataView):
            return obj.to_json()
        elif isinstance(obj, H5FileView):
            return obj.to_json()
        return json.JSONEncoder.default(self, obj)


class H5DataView:

    def __init__(self, flat_layout=True) -> None:
        self.prefix = 'CONTROL'
        self.flat_layout = flat_layout
        self.data = {self.prefix: {}}
        pass

    def __call__(self, name, h5obj):
        if isinstance(h5obj, h5py.Dataset):
            self.insert_path(name, {"metadata": "meta data"})

    def __str__(self) -> str:
        return str(self.data)

    def to_json(self):
        return self.data

    def insert_path(self, name, metadata):
        name = self.sanitize_name(name)
        if self.flat_layout:
            self.data[self.prefix][name] = metadata
            return

        parent = self.data
        key = self.prefix
        cursor = parent.get(key, {})
        for p in name.split('/'):
            if p in {'MDL'}:
                continue
            if p not in cursor:
                cursor[p] = {}

            parent = cursor
            key = p
            cursor = parent.get(key, {})
        parent[key] = metadata

    def get_metadata(self, name):
        name = self.sanitize_name(name)
        if self.flat_layout:
            return self.data[self.prefix].get(name)

        parent = self.data
        key = self.prefix
        cursor = parent.get(key, {})
        for p in name.split('/'):
            if p in {'MDL'}:
                continue
            if p not in cursor:
                return None
                return {"error": f"Path does not exist, starting from {p}"}
            parent = cursor
            key = p
            cursor = parent.get(key)
        return cursor

    def sanitize_name(self, name):
        return name.removeprefix(self.prefix + '/').removesuffix('/value').removesuffix('/timestamp')


class H5FileView:
    def __init__(self, prefix="CONTROL"):
        self.prefix = prefix
        self.data = {}

    def __call__(self, filename):
        if h5py.is_hdf5(filename):
            data_view = self.register_file(filename)
            try:
                with h5py.File(filename, 'r') as f:
                    # this will visit all objects inside the hdf5 file and store datasets in data_view object (ie names)
                    f["CONTROL"].visititems(data_view)
            except Exception as e:
                logger.error(e)
        else:
            raise SystemError(f"Invalid HDF5 file: {filename}")

    def __str__(self) -> str:
        return str(self.data)

    def to_json(self):
        return self.data

    def register_file(self, filename):
        self.data[str(filename)] = H5DataView(flat_layout=True)
        return self.data.get(str(filename))
