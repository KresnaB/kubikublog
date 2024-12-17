import os
import re
import shutil

# Paths (use raw strings to handle backslashes correctly in Windows)
posts_dir = r"C:\Users\kresn\Documents\kubikublog\content\posts"
attachments_dir = r"C:\Users\kresn\Obsidian Vault\kresna\Images"
static_images_dir = r"C:\Users\kresn\Documents\kubikublog\static\images"

# Create the static/images directory if it doesn't exist
os.makedirs(static_images_dir, exist_ok=True)

# Step 1: Process each markdown file in the posts directory
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        print(f"Processing: {filename}")
        
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Step 2: Find all Obsidian-style image links [[Image.png]]
        images = re.findall(r'\[\[([^]]+\.(?:png|jpg|jpeg|svg))\]\]', content)
        
        if images:
            print(f"  Found images: {images}")
        
        # Step 3: Replace image links and ensure URLs are correctly formatted
        for image in images:
            # Encode spaces with %20 for Markdown compatibility
            markdown_image = f"![Image Description](/images/{image.replace(' ', '%20')})"
            content = content.replace(f"[[{image}]]", markdown_image)
            
            # Step 4: Copy the image to the Hugo static/images directory
            image_source = os.path.join(attachments_dir, image)
            image_destination = os.path.join(static_images_dir, image)
            
            if os.path.exists(image_source):
                if not os.path.exists(image_destination):
                    shutil.copy(image_source, image_destination)
                    print(f"    Copied: {image} to {static_images_dir}")
                else:
                    print(f"    Skipped: {image} (already exists in destination)")
            else:
                print(f"    Warning: {image} not found in {attachments_dir}")
        
        # Step 5: Write the updated content back to the markdown file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print("All markdown files processed and images handled successfully.")
