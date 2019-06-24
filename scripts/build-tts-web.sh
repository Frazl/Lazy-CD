#Example script
cd tts-web
npm install 
npm run build 
rm -r -f /var/www/tts
mv /build /var/www/tts
cd ..
echo "Completed"
