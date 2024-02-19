"""
vis.py
Visualization tools.

Author        : Dylan Martins
Written       : Nov 09 2023
Last modified : Jan 26 2024
"""


import matplotlib.pyplot as plt
import matplotlib.animation as animation



def make_WF_animation(dFF):
    """ Make an animation of the dF/F values for a widefield image stack.

    This is VERY slow.

    Parameters
    ----------
    dFF : np.ndarray
        dF/F values for each pixel in the image stack over
        time, with the shape (frames, height, width).
    """

    # create a figure and axis object
    fig, ax = plt.subplots()

    # define the update function for the animation
    def update(i):
        ax.imshow(dFF[i,:,:], cmap='gray')
        ax.set_title(f'Frame {i}')
        return ax

    # create the animation object
    ani = animation.FuncAnimation(fig, update, frames=dFF.shape[0], interval=100)

    # save the animation as an .avi file
    ani.save('dFF_animation.avi', writer='ffmpeg')


