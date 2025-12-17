import os
import copy

def main(**kwargs):
    #clone or pull oomlout_oompbuilder into temporary/oomlout_oomp_builder
    repo_url = "https://github.com/oomlout/oomlout_oomp_builder_limited"
    repo_dir = "temporary\\oomlout_oomp_builder_limited"
    if not os.path.exists(repo_dir):
        os.system(f"git clone {repo_url} {repo_dir}")
    else:
        os.system(f"cd {repo_dir} && git pull")

    #check the configuration directory exists and isn't empty
    config_dir = "configuration"
    if not os.path.exists(config_dir) or not os.listdir(config_dir):
        input("Configuration directory is empty or doesn't exist. Press enter to continue to copy default build configuration")
        #copy the default build configuration to the configuration directory in windows
        command = f"copy {repo_dir}\\configuration {config_dir}"
        print(command)
        os.system(command)
        

    #copy all files that have been changed or created in the last hour from C:\gh\oomlout_oomp_part_generation_version_1\parts to parts
    if True:
        import time
        import shutil
        source_dir = r"C:\gh\oomlout_oomp_part_generation_version_1\parts"
        dest_dir = "parts"
        
        if os.path.exists(source_dir):
            current_time = time.time()
            one_hour_ago = current_time - 3600
            copied_count = 0
            
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    source_file = os.path.join(root, file)
                    if os.path.getmtime(source_file) > one_hour_ago:
                        # Calculate relative path and destination
                        rel_path = os.path.relpath(source_file, source_dir)
                        dest_file = os.path.join(dest_dir, rel_path)
                        
                        # Create destination directory if needed
                        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                        
                        # Copy the file
                        shutil.copy2(source_file, dest_file)
                        copied_count += 1
            
            print(f"Copied {copied_count} files from {source_dir} that were modified in the last hour")
        else:
            print(f"Source directory {source_dir} does not exist, skipping copy")

    #before running rename parts directory parts_2
    if True:
        if os.path.exists("parts"):
            if os.path.exists("parts_2"):
                os.system("powershell -Command \"Remove-Item -Path 'parts_2' -Recurse -Force\"")
            #wait for it to finish
            os.system("powershell -Command \"Move-Item -Path 'parts' -Destination 'parts_2' -Force\"")
            

    #look at all the files in parts two, find any that have been created in the last hour
    if True:
        import time
        current_time = time.time()
        one_hour_ago = current_time - 3600
        recent_files = []
        if os.path.exists("parts_2"):
            for root, dirs, files in os.walk("parts_2"):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.getmtime(file_path) > one_hour_ago:
                        recent_files.append(file_path)
        print(f"Found {len(recent_files)} files created in the last hour")
        #move the new file to parts directory
        for file_path in recent_files:
            rel_path = os.path.relpath(file_path, "parts_2")
            dest_file = os.path.join("parts", rel_path)
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            shutil.copy2(file_path, dest_file)
    
    #run the oomp stuff
    if True:
        #import run.py from the cloned repo
        import sys
        sys.path.append(repo_dir)
        import run_limited
        run_limited.main(**kwargs)

    #move the parts from parts to parts_2 then remove parts using os.system
    if True:
        if os.path.exists("parts_2"):
            
            os.system("powershell -Command \"Move-Item -Path 'parts' -Destination 'parts_2' -Force\"")
            os.system("powershell -Command \"Remove-Item -Path 'parts' -Recurse -Force\"")


            

    #rename parts_2 back to parts
    if True:
        if os.path.exists("parts_2") and not os.path.exists("parts"):
            os.system("powershell -Command \"Move-Item -Path 'parts_2' -Destination 'parts' -Force\"")


    #git commit changes
    if True:
        #check to make sure less than 100 files are changed
        changed_files = os.popen("git diff --name-only").read().strip().split('\n')
        if len(changed_files) < 100:
            os.system("git add .")
            commit_message = "Automated commit of built parts"
            os.system(f'git commit -m "{commit_message}"')
            #os.system("git push")
        else:
            print("Too many files changed, not committing.")

if __name__ == '__main__':
    #add args parse and add a filter -f option
    import argparse
    parser = argparse.ArgumentParser(description="Build OOMP parts using oomlout_oomp_builder.")
    parser.add_argument('-f', '--filter', type=str, default="", help="Filter for the build process.")
    args = parser.parse_args()
    #convert args to kwargs
    kwargs = copy.deepcopy(vars(args))
    print(f"kwargs: {kwargs}")
    #test filter with printer
    #kwargs["filter"] = "printer"
    #kwargs = {}
    main(**kwargs)