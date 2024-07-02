# Ask for image URLs
read -p "Provide image URL here (separate multiple with semicolons): " input

# Convert the input string into an array of URLs, using semicolon as the delimiter
IFS=';' read -r -a urls <<< "$input"

# Create or empty the folders
mkdir -p ./temp
mkdir -p ./square && rm -f ./square/*

# Initialize a counter for naming the images
counter=1

# Download each image from the provided URLs
for url in "${urls[@]}"
do
  # Trim leading and trailing whitespace
  url=$(echo $url | xargs)

  # Download the image to the temp directory with a name based on the counter
  curl -o "./temp/image$counter.jpg" "$url"

  # Increment the counter
  ((counter++))
done

# Reset counter for naming and counting the processed images
counter=1

# Process each downloaded image
for file in ./temp/*
do
  # Name the processed file based on the counter
  keyOut="image$counter-sq.jpg"

  # Process the image
  convert "$file" -background white -gravity center -resize 600X600 -extent 1000X1000 "./square/$keyOut"

  # Increment the counter
  ((counter++))
done

# Clean up temp directory
rm -r ./temp

# Display success message
echo "Successfully squared $((counter-1)) images, stored in folder: 'square'"

