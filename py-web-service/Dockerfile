FROM base/archlinux
RUN pacman --noconfirm -Syu python reflector
RUN reflector --country Germany --latest 10 --protocol https --sort rate --save /etc/pacman.d/mirrorlist

RUN pacman --noconfirm -S python-pip git vim sox ffmpeg
RUN pip install Flask python-dotenv gTTS pydub

WORKDIR /app

ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"]
EXPOSE 5000
