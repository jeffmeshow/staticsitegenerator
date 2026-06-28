import os
from config import MAX_CHARS, CONTENT_DIR, PUBLIC_DIR
from parsemarkdown import markdown_to_blocks, parse_title_text
from parseblocks import markdown_to_html_node


def get_files_r(abs_directory: str, files: list[str]) -> list[str]:

    if files is None:
        files = []
    for item in os.listdir(abs_directory):
        item_abs = os.path.normpath(os.path.join(abs_directory, item))
        if os.path.isdir(item_abs):
            get_files_r(item_abs, files)
        else:           
            files.append(item_abs)    
    return files


def generate_pages(from_dir: str, template_path: str):
    pages: list[(str, str)] = []
    from_files: list[str] = []
    working_abs_directory = os.path.abspath(".")    
    from_abs_directory = os.path.normpath(os.path.join(working_abs_directory, from_dir))     
    #dest_abs_directory = os.path.normpath(os.path.join(working_abs_directory, dest_dir)) 
    from_files = get_files_r(from_abs_directory, from_files)


    for file in from_files:
        from_path = file.replace(from_abs_directory + "/", "")
        dest_path = from_path.replace(".md", ".html")
        generate_page(from_path, template_path, dest_path)


def generate_page(from_path: str, template_path: str, dest_path:str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    page = get_file_content(CONTENT_DIR, from_path)
    template = get_file_content(".", template_path)
    title = parse_title_text(page)
    nodes = markdown_to_html_node(page)
    html = nodes.to_html()

    content = template.replace("{{ Title }}", title)
    content = content.replace("{{ Content }}", html)
    
    write_file(PUBLIC_DIR, dest_path, content)



def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)    
        target_path = os.path.normpath(os.path.join(working_directory_abs, file_path))     
        parent_dir = os.path.dirname(target_path)

        if os.path.commonpath([working_directory_abs, target_path]) != working_directory_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        if not os.path.isdir(parent_dir):
            os.makedirs(parent_dir, 0o755, True)

        written_length = 0
        with open(target_path, "w") as f:
            written_length = f.write(content)
        
        if written_length > 0:
            print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
        else:
            print(f'Nothng written to "{file_path}"')

    except Exception as e:
        print(f'Error: Encountered problem writie to file "{file_path}": {e}')

def get_file_content(working_directory: str, file_path: str) -> str:

    file_content_string:str = ""
    was_trucated:bool = False

    try:
        working_directory_abs = os.path.abspath(working_directory)    
        target_path = os.path.normpath(os.path.join(working_directory_abs, file_path))        

        if os.path.commonpath([working_directory_abs, target_path]) != working_directory_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'   
    
        # if we got this far, it's a valid file        
        with open(target_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1) != "":
                file_content_string +=  f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content_string
    
    except Exception as e:
        return f'Error: Encountered problem reading file "{file_path}": {e}'

