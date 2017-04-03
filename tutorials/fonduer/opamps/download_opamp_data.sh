echo "Downloading opamp data..."
url=https://stanford.box.com/shared/static/ihaqmjlg96n589943yssb54ufogjycp8.zip
data_zip=opamp_dataset

wget -N -O opamp_dataset.zip -q --show-progress $url

echo "Unpacking opamp data..."
unzip -o  $data_zip.zip -d data

echo "Deleting zip file..."
rm $data_zip.zip

echo "Done!"
