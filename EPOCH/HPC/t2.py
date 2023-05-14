import os


def remove_all_sdf_files():
    # Remove all files ending with .sdf recursively
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".sdf"):
                os.remove(os.path.join(root, file))


def zip_dir():
    # zip the whole directory recursively but exclude any files ending with .sdf

    import zipfile

    zipf = zipfile.ZipFile("all_data.zip", "w", zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk("."):
        for file in files:
            if not file.endswith(".sdf"):
                zipf.write(os.path.join(root, file))
    zipf.close()


if __name__ == "__main__":
    # remove_all_sdf_files()
    zip_dir()