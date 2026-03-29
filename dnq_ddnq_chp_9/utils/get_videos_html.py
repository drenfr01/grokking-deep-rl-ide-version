import numpy as np
import io
import base64
import json

def get_videos_html(env_videos, title, max_n_videos=5):
    videos = np.array(env_videos)
    if len(videos) == 0:
        return
    
    n_videos = max(1, min(max_n_videos, len(videos)))
    idxs = np.linspace(0, len(videos) - 1, n_videos).astype(int) if n_videos > 1 else [-1,]
    videos = videos[idxs,...]

    strm = '<h2>{}<h2>'.format(title)
    for idx, (video_path, meta_path) in enumerate(videos):
        video = io.open(video_path, 'r+b').read()
        encoded = base64.b64encode(video)

        episode_id = idx
        if meta_path:
            with open(meta_path) as data_file:
                meta = json.load(data_file)
            episode_id = meta.get('episode_id', idx)

        html_tag = """
        <h3>{0}<h3/>
        <video width="960" height="540" controls>
            <source src="data:video/mp4;base64,{1}" type="video/mp4" />
        </video>"""
        strm += html_tag.format('Episode ' + str(episode_id), encoded.decode('ascii'))
    return strm