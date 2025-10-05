# Añadir las librerías necesarias

# Librerías esenciales
import sys
import yaml
import pickle

def train(data, n1_arg, n2_arg):

    # Aquí va la pipeline de entrenamiento del modelo

    return None

def main():

    # Cargar parámetros desde params.yaml
    params = yaml.safe_load(open("params.yaml"))["train"]

    # Confirmar que la cantidad de argumentos es correcta (data_path, n_args de train, model_path)
    if len(sys.argv) != len(train.__code__.co_varnames) + 1:
        sys.stderr.write("Arguments error. Usage:\n")
        sys.stderr.write("    python train.py <data_path> <model_path>\n")
        sys.exit(1)
    
    input = sys.argv[1]
    output = sys.argv[2]

    # CAMBIAR ESTO SEGÚN LOS ARGUMENTOS DE LA FUNCIÓN train
    n1_arg = params["n1_arg"]
    n2_arg = params["n2_arg"]

    # Llamar a la función train con los argumentos necesarios
    clf = train(input, n1_arg, n2_arg)

    # Guardar el modelo entrenado en output
    with open(output, "wb") as f:
        pickle.dump(clf, f)

if __name__ == "__main__":
    main()