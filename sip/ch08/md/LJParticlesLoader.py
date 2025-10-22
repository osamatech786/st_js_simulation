import pickle

def save_state(model, filename="lj_particles_state.pkl"):
    """
    Saves the state of the LJParticles model to a file.
    
    :param model: The LJParticles model instance.
    :param filename: The name of the file to save the state to.
    """
    with open(filename, 'wb') as f:
        pickle.dump(model, f)

def load_state(filename="lj_particles_state.pkl"):
    """
    Loads the state of the LJParticles model from a file.
    
    :param filename: The name of the file to load the state from.
    :return: The loaded LJParticles model instance.
    """
    with open(filename, 'rb') as f:
        return pickle.load(f)
