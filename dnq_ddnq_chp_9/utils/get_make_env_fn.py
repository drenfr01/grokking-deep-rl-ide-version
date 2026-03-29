import tempfile
import gymnasium as gym
from gymnasium import wrappers

def get_make_env_fn(**kargs):
    def make_env_fn(env_name, seed=None, render=None, record=False,
                    unwrapped=False, monitor_mode=None, 
                    inner_wrappers=None, outer_wrappers=None):
        mdir = tempfile.mkdtemp()
        env = None
        if render:
            render_mode = render if isinstance(render, str) else 'rgb_array'
            try:
                env = gym.make(env_name, render_mode=render_mode)
            except TypeError:
                # Backward compatibility for older Gym APIs.
                try:
                    env = gym.make(env_name, render=render)
                except Exception:
                    pass
            except Exception:
                pass
        if env is None:
            env = gym.make(env_name)
        if seed is not None:
            # Gymnasium removed env.seed(); seed via reset instead.
            try:
                env.reset(seed=seed)
            except TypeError:
                # Backward compatibility for older Gym versions.
                if hasattr(env, "seed"):
                    env.seed(seed)
            if hasattr(env.action_space, "seed"):
                env.action_space.seed(seed)
        env = env.unwrapped if unwrapped else env
        if inner_wrappers:
            for wrapper in inner_wrappers:
                env = wrapper(env)
        env = wrappers.RecordVideo(
            env,
            video_folder=mdir,
            episode_trigger=lambda _episode_id: bool(record),
            name_prefix=str(monitor_mode),
        ) if monitor_mode else env
        if outer_wrappers:
            for wrapper in outer_wrappers:
                env = wrapper(env)
        return env
    return make_env_fn, kargs