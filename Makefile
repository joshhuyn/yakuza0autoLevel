run: *
	./venv/bin/python ./Main.py

clean:
	rm imgCache/*

view:
	gwenview ./imgCache/resized.png
