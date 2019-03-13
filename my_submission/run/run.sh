
INPUT_DATA="somewhere/data" # CHANGE TO YOUR LOCAL DIRECTORY WITH DATA (hits, cells, and truth csv files)

docker run -i --rm \
	-v $(pwd):/home/code \
	-v $INPUT_DATA:/home/data \
	estradevictorantoine/trackml:1.0 \
	/bin/sh -c "cd /home/code; python main.py $*"
