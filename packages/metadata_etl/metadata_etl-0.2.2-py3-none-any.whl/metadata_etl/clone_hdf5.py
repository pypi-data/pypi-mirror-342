import h5py


def clone_datasets_simple(source_file, target_file, datasets):
    with h5py.File(target_file, 'w') as f_trgt, h5py.File(source_file, 'r') as f_src:
        f_src.copy(f_src[f'METADATA'], f_trgt)
        for dataset in datasets:
            print(dataset)
            group_path = f_src[dataset].parent.name
            for member in f_src[group_path]:
                if isinstance(f_src[f'{group_path}/{member}'], h5py.Dataset):
                    f_src.copy(f_src[f'{group_path}/{member}'], f_trgt, f'{group_path}/{member}')


def clone_datasets_special(source_file, target_file, datasets):
    with h5py.File(target_file, 'w') as f_trgt, h5py.File(source_file, 'r') as f_src:
        f_src.copy(f_src[f'METADATA'], f_trgt)

        for dataset in datasets:
            # Get the name of the parent for the group we want to copy
            group_path = f_src[dataset].parent.name
            print(dataset)
            group_id = f_trgt.require_group(group_path)

            for member in f_src[group_path]:
                src_dataset = f_src[f'{group_path}/{member}']
                shape = src_dataset.shape
                dtype = src_dataset.dtype
                attrs = src_dataset.attrs

                print(attrs.keys())

                print(shape)
                ds_arr = f_src[f'{group_path}/{member}'][:]
                ds = f_trgt.create_dataset(f'{group_path}/{member}', data=f_src[f'{group_path}/{member}'][:10])

                attrs = ds.attrs
                attrs.update(src_dataset.attrs)
                print(attrs.keys())
