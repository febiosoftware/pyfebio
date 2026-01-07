import h5py

def print_datasets(name, obj):
    if isinstance(obj, h5py.Dataset):
        print(name, f"shape: {obj.shape}", f"dtype: {obj.dtype}")

f = h5py.File("elastic_hex20.hdf5", "r")
# view all the datasets and their shape and dtype
f.visititems(print_datasets)

# shared attributes are stored at the appropriate parent group
# e.g. the time at a given state can be accessed as follows:
print("\n Time at state 5")
print(f["/states/5"].attrs["time"])

# to view the data in a Dataset
print("\n Displacement at state 5")
print(f["/states/5/node_data/displacement/1"][:])

# this is simply a numpy array so we can also slice it
print("\n Displacement at state 5 of first 2 nodes")
print(f["/states/5/node_data/displacement/1"][0:2,:])
# the nice thing about this though is HDF5 uses lazy loading
# which means that the data is not loaded into memory until it is accessed
# this is useful for large datasets that do not fit into memory

f.close()
