for %%f in (*) do (ffmpeg -i "%%f" -vf scale=350:-1 thumbnails/%%~nf.jpg)
