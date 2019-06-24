#Example script
mkdir tmp
cd ./tts-flask
rm -f players
rm -f players.csv
set +e
cp  ../tts-flask/matches.csv ./tmp/matches.csv
cp -r -f ../tts-flask/players/* ./tmp/players/
rm -r -f ../tts-flask
cp -r ./tts-flask /home/main/tts-flask
cp -r -f ./tmp/players/* ../tts-flask/players
cp -r -f ./tmp/matches.csv ../tts-flask/matches.csv
supervisorctl restart tts
