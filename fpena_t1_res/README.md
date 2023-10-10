¡¡¡ESTA CARPETA ES NECESARIA PARA EL FUNCIONAMIENTO DEL CODIGO DE LA TAREA 1!!!

DENTRO VIENEN LOS SIGUIENTES ARCHIVOS:

A_shader.frag:
    contiene el codigo del fragment shader utilizado para los meshes de color

A_shader.vert:
    contiene el codigo del vertex shader utilizado para los meshes de color

X_Camera: 
    contiene la clase para crear camaras. Por algun motivo, OrbitCamera no funciona,
    asi que no se ha de instanciar dentro de la tarea.

X_Mesh:
    contiene la clase para crear meshes, que instancia de X_Model

X_Model: 
    contiene la clase para crear modelos. Contiene los metodos para dibujar e inicializar la
    data de un modelo en gpu.

X_SceneGraph:
    contiene la clase para crear grafos de escena. ¡¡¡REQUIERE INSTALAR networkx EN EL ENTORNO
    VIRTUAL SOBRE EL QUE SE CORRE LA TAREA!!!. Instalar mediante 
    
    %pip install networkx 
    
    en la consola abierta sobre el entorno virtual en el que se corre la tarea.

car_tired:
    contiene el modelo del auto y de las llantas en formato glb. Lo hice yo mismo en 
    Blender. De requerirlo, me pueden pedir el modelo en formato .blend para abrirlo
    en la aplicacion. Se llama car_tired porque es un auto al que se le han agregado llantas.

ca_car:
    clase que instancia el auto. Hace uso de X_Model y X_SceneGraph para este fin. Contiene los
    metodos draw(self) y update(self, total_time).

        draw(self):
            dibuja el auto en pantalla.

        update(self, total_time):
            actualiza el modelo de acuerdo al tiempo total que lleva corriendo el programa.

COMO FUNCIONA LA TAREA 1:
    1.- se importa todo lo que es necesario importar

    2.- se crea una variable para almacenar el tiempo total que lleva corriendo el programa, 
        esto es necesario para actualizar el modelo del auto.

    3.- se crea una camara. Esta debe ser una instancia de X_Camera.Camera, debido a que 
        X_Camera.OrbitCamera no funciona. El auto rota solo, asi que no es necesaria tampoco.
    
    4.- se crea el pipeline del auto con los shaders proporcionados.

    5.- se instancia el auto. Pueden pintarlo de acuerdo a su preferencia.

    6.- la funcion update actualiza el tiempo total y llama a la funcion update del auto.
    
    7.- la funcion on_draw limpia la ventana, configura OpenGL. Llama a la funcion
        draw del auto.

    8.- se corre el programa en intervalos de 1/60 de segundo. Se llama a la funcion 
        update cada intervalo.

DE BUSCAR MAYOR INFORMACION ACERCA DE COMO SE INSTANCIAN LOS VERTICES DEL AUTO, REVISAR
LA CLASE ca_car.