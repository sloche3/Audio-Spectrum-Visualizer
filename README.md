# Audio-Spectrum-Visualizer
**NOTE:** This may not work as well on some devices depending on the device's microphone.

## Import notes
- PyAudio is used to receive live audio from the device's default audio input
- PyQtGraph is used to plot the frequency data, and it also requires PyQt to function.
  I decided to use this over matplotlib because it sounded like PyQtGraph was faster/better
  at plotting real time data.
  
## Things that still need to be looked at
- While PyAudio does allow you to receive audio in real time, my end goal is to be able 
  to use the device output as an input. For example, music playing on the device could be used to 
  generate the graph results. But apparently PyAudio can't help me with that. I tried using windows'
  stereo mix, but the graph never seems very clean when I use it, like it's constantly picking up
  on some fantom audio. And both, stereo mix and the microphone, seem to be very sensitive, so you have
  to turn them down very low to see any kind of "decent" results (microphone input literally has to be
  set to 1, and you have to lower output volume to like 2 for stereo mix). I think I need to look into 
  an audio loopback device or something to solve this problem.
  - **NOTE:** Did some sound tests, and I don't think the mic sensitivity will actually be a problem
    for what I want to do with this. So for now, this will be ignored.
- ~~I'd like to see if there is a way to get rid of the X and Y axis. I don't really care for the 
  measurements, I'm just interested in the visual.~~ **DONE**
  
## Possible future improvements to look into
- Changing line colors at certain frequencies.
- I'm not sure if this could even be applied, but maybe add the option to use another shape, like a 
  circle instead of a line.
- ~~Do something cool with the background (different colors? sound reactive movement? idk).~~ 
  **Added Tie-Dye**
  
**NOTE:** I don't plan on looking into these features anymore...for now...

## Resources
There were others, but I went through a lot of stuff, and closed a lot of tabs..
- [PyQtGraph documentation](https://pyqtgraph.readthedocs.io/en/latest/)
- [PyAudio documentation](https://people.csail.mit.edu/hubert/pyaudio/docs/)
- [How do music visualizers work?](https://www.reddit.com/r/explainlikeimfive/comments/1l2gof/eli5_how_do_music_visualizers_work/)
- [Mark Jay (YouTube)](https://www.youtube.com/watch?v=RHmTgapLu4s)
- [Mark Jay's github project](https://github.com/markjay4k/Audio-Spectrum-Analyzer-in-Python/blob/master/audio_spectrumQT.py)
- I don't think I ended up using this but, [Plotting with matplotlib example](https://stackoverflow.com/questions/18625085/how-to-plot-a-wav-file)
- [Qt window settings](https://doc.qt.io/qt-6/qt.html#WindowType-enum)