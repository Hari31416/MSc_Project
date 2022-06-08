import os
import shutil
import nbformat
from nbconvert import HTMLExporter
import re
import tqdm


class FileOrganizer:
    """
    A class used for some tools related to file organization.

    Attributes
    ----------
    directory : str
        The directory where the files are located.

    Methods
    -------
    change_directory(directory)
        Changes the directory of the class.

    remove_spaces(formats=None, category=None)
        Removes the spaces from all the files in the directory with the \\
        provided formats or all the formates corresponding to the given\\
        category.

    add_file_kinds(kind, formats)
        Adds another category to the list of categories.

    everything_in_directory()
        Return two lists with all files and folders in directory.

    files_in_directory()
        Returns a list of all files in the directory.

    folders_in_directory()
        Returns a list of all folders in the directory.

    walk_through_directory(directory)
        A function that walks through a directory and prints the name of each file,
        folder and subfolder in the directory.

    rename_file(original_name, new_name, directory)
        Renames a file.

    calculate_directory_size(directory)
        Calculates the size of a directory.

    organize_by_format(directory)
        Organizes the files in the directory by their format.

    organize_directory()
        A function to organize the directory.
    """

    def __init__(self, directory=os.curdir) -> None:
        self.directory = directory
        self.files_in_category = {
            "images": ["jpg", "jpeg", "png", "gif", "bmp"],
            "videos": ["mp4", "mkv", "avi", "flv", "wmv", "mov"],
            "audio": ["mp3", "wav", "flac", "ogg", "aac"],
            "documents": ["pdf", "doc", "docx", "ppt", "pptx"],
            "archives": ["zip", "rar", "7z", "tar", "gz", "bz2", "7z", "iso"],
            "applications": ["exe", "msi", "deb", "rpm", "dmg", "pkg"],
            "ebooks": ["epub", "mobi", "fb2"],
            "data": ["xls", "xlsx", "csv", "json"],
            "others": ["txt", "torrent", "srt", "sub"],
        }

    def change_directory(self, directory):
        """
        Changes the directory of the class.

        Parameters
        ----------
        directory : str
            The new directory of the class.

        Returns
        -------
        None
        """
        if os.path.isabs(directory):
            self.directory = directory
        else:
            self.directory = os.path.join(self.directory, directory)

    def remove_spaces(self, all=False, formats=None, category=None):
        """
        Removes the spaces from all the files in the directory with the \\
        provided formats or all the formates corresponding to the given\\
        category.

        Parameters
        ----------
        formates : list
            The list of formats.

        Returns
        -------
        None
        """
        if all:
            for folder, _, files in os.walk(self.directory):
                for file in files:
                    file_name = os.path.join(folder, file)
                    new_file_name = file_name.replace(" ", "_")
                    os.rename(file_name, new_file_name)
            return None

        if not formats and not category:
            print("Please provide a list of formats or a category")
            return None
        elif formats:
            formats = formats.copy()
        else:
            formats = self.files_in_category[category].copy()

        for folder, _, files in os.walk(self.directory):
            for file in files:
                for format in formats:
                    if file.endswith(format):
                        file_name = os.path.join(folder, file)
                        new_file_name = file_name.replace(" ", "_")
                        os.rename(file_name, new_file_name)

    def add_file_kinds(self, kind, formats=[]):
        """
        Adds another category to the list of categories.

        Parameters
        ----------
        kind : str
            The name of the new category.

        formats : list
            The list of file formats that belong to the new category.

        Returns
        -------
        None
        """
        self.files_in_category[kind] = formats
        print(f"Added {kind} to the dictionary of categories")

    def add_formats(self, formats, category="others"):
        """
        Adds a list of formats to the list of categories.

        Parameters
        ----------
        formats : list
            The list of file formats that belong to the provided category.

        category : str
            The name of the category.
        """
        if category in self.files_in_category.keys():
            self.files_in_category[category] += formats
            print(f"Added {formats} to the {category} category")
        else:
            self.add_file_kinds(category, formats)

    def get_file_formats(self, category="others"):
        """
        Returns the list of formats belonging to the provided category.

        Parameters
        ----------
        category : str
            The name of the category.

        Returns
        -------
        list
            The list of formats belonging to the provided category.
        """
        return self.files_in_category[category]

    def everything_in_directory(self):
        """
        Return two lists with all files and folders in directory.\\
        To be used later

        Parameters
        ----------
        None

        Returns
        -------
        lists
            Two list containing all folders in the directory.
        """
        items = os.listdir(self.directory)
        folders = []
        files = []
        for item in items:
            is_directory = os.path.isdir(os.path.join(self.directory, item))
            if not is_directory:
                files.append(item)
            else:
                folders.append(item)
        return folders, files

    def files_in_directory(self):
        """
        Returns a list of all files in the directory.

        Parameters
        ----------
        None

        Returns
        -------
        list
            The list of all files in the directory.
        """
        folders, files = self.everything_in_directory()
        return files

    def folders_in_directory(self):
        """
        Returns a list of all folders in the directory.

        Parameters
        ----------
        None

        Returns
        -------
        list
            The list of all folders in the directory.
        """
        folders, files = self.everything_in_directory()
        return folders

    def walk_through_directory(self):
        """
        A function that walks through a directory and prints the name of each file,
        folder and subfolder in the directory.

        Parameters
        ----------
        directory : str
            The directory to walk through.

        Returns
        -------
        None

        Example:
            >>> walk_through_directory('/home/user/Desktop')
        """
        for folder, subfolder, files in os.walk(self.directory):
            print(f"Current Folder: {folder}")
            print("Subfolders:", subfolder)
            for file in files:
                print(file)

    def rename_file(self, original_name, new_name, directory):
        """
        Renames a file.

        Parameters
        ----------
        original_name : str
            The name of the file to be renamed.

        new_name : str
            The new name of the file.

        directory : str
            The directory where the file is located.

        Returns
        -------
        None

        """
        os.rename(
            os.path.join(directory, original_name),
            os.path.join(directory, new_name),
        )

    def organize_by_format(self, formats, destination, directory=None):
        """
        A function to organize files by format, eg. by images, videos, audio, etc.\\
        The functions organizes all the files with some specific format in a\\
        specific folder. These files need not be in the parent directory, the\\
        function will walk through the whole directory.

        Parameters
        ----------
        directory : str
            The directory which we need to organize. If not provided, uses class attribute
        formats : list
            A list of file formats to organize.
        destination : str
        The destination directory to move the files to.

        Returns
        -------
            None
            
        Example:
            >>> organize_by_format("/home/user/Desktop/", ["jpg", "png"], "/home/user/Desktop/images")
        """
        # Changing the directory if it is provided
        if directory is not None:
            self.change_directory(directory)

        new_dir = os.path.join(self.directory, destination.title())
        if not os.path.exists(new_dir):
            print("Creating the directory: ", new_dir)
            os.mkdir(new_dir)
        else:
            print("Directory already exists")

        for folder, subfolder, files in os.walk(self.directory):
            print(f"Current Folder: {folder}")
            for file in files:
                if folder == new_dir:
                    continue
                for format in formats:
                    if file.endswith(format):
                        original_dir = os.path.join(folder, file)
                        try:
                            shutil.move(original_dir, new_dir)
                        except shutil.Error:
                            print(f"File {file} already exists in {new_dir}")

        print("Organization complete!")

    def calculate_directory_size(
        self,
        directory=None,
        output_unit="kb",
        exclude_files_by_format=None,
        exclude_files_by_size=None,
        exclude_files_units=None,
        number_of_files=False,
    ):
        """
        A function to calculate the size of a directory.

        Parameters
        ----------
        directory : str
            The directory to calculate the size of. If not provided, ues class attribute.
        
        output_unit : str
            The unit to output the size in. Default is kb.\\
            valid units are: b, kb, mb and gb
        
        exclude_files_format: list
            A list of file formats to exclude from the size calculation.\\
            Default is None.

        exclude_files_size: int
            Every file with a size smaller than this value will be excluded\\
            from the size calculation. Default is `None`.\\
            The unit of the size is specified by the `exclude_files_units` argument. If not, it's assumed\\
            to be same as the `output_unit`.
        
        exclude_files_units: str
            The unit of the exclude_files_size argument.\\
            Default is kb. valid units are: b, kb, mb and gb
    
        number_of_files: bool 
            If True, the number of files in the directory will also be returned.\\
            Note: Only those files which are not excluded will be counted.

        Returns
        -------
        int/tuple of two ints
            The size of the directory in units of `output_unit`.

        Example
        -------
            >>> calculate_directory_size("/home/user/Desktop/", "mb", ["jpg", "png"], 100)
        """
        # Initialize the total_size variable
        total_size = 0
        num_files = 0
        files_excluded = 0

        # Creating a conversion dictionary
        conversion_dict = {
            "b": 1,
            "kb": 1024,
            "mb": 1024 ** 2,
            "gb": 1024 ** 3,
            None: 1024,
        }

        try:
            # Get the output unit conversion factor
            output_unit_factor = conversion_dict[output_unit.lower()]

            # Get the exclude_files_size conversion factor
            if exclude_files_units is not None:
                exclude_files_size_factor = conversion_dict[exclude_files_units.lower()]
            else:
                exclude_files_size_factor = output_unit_factor
        except KeyError:
            print("Invalid output_unit")
            print("Valid units are: b, Kb, Mb and Gb")
            return None

        # Changing the directory if it is provided
        if directory is not None:
            self.change_directory(directory)

        for folder, _, files in os.walk(self.directory):
            for file in tqdm.tqdm(files, desc="Calculating..."):
                try:
                    file_size = os.path.getsize(os.path.join(folder, file))
                except Exception as e:
                    print(e)
                    print("Ignoring the size of this file.")
                    file_size = 0

                # Excluding the files with the specified format
                if exclude_files_by_format is not None:
                    for format in exclude_files_by_format:
                        if file.endswith(format):
                            files_excluded += 1
                            file_size = 0
                            num_files += 0
                            break

                # Excluding the files with the specified size
                if exclude_files_by_size is not None:
                    if file_size < exclude_files_by_size * exclude_files_size_factor:
                        files_excluded += 1
                        file_size = 0
                        num_files += 0

                total_size += file_size
                num_files += 1

        total_file_size = round(total_size / output_unit_factor, 2)

        # Printing number of excluded files
        if exclude_files_by_format or exclude_files_by_size:
            print(f"Total number of files excluded is: {files_excluded}")

        # Printing the outputs
        if number_of_files:
            print(
                f"The size of the directory is: {total_file_size} {output_unit.title()}"
            )
            print(f"The number of files in the directory is: {num_files}")
            print(
                f"Numbers of files included in the size calculation: {num_files - files_excluded}"
            )
            return total_file_size, num_files
        else:
            print(
                f"The size of the directory is: {total_file_size} {output_unit.title()}"
            )
            return total_file_size

    def organize_directory(self):
        """
        A function to organize the directory.\\
        The function organizes the files in the directory according to their\\
        extensions.

        Returns
        -------
            None
        """
        for key, value in self.files_in_category.items():
            self.organize_by_format(value, key)
