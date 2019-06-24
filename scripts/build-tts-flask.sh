#Example script
mkdir tmp 
cp ../tts-flask/matches.csv ./tmp/matches.csv
cp ../tts-flask/players ./tmp/players
cp ./tts-flask ../
supervisorctl restart tts