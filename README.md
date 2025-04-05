# Prueba Técnica

Las contraseñas y datos sensibles fueron eliminados

## Github action que al commitear ejecute un trigger que: 

- Cree un workflow de github actions para compilar y publicar una imagen de docker 
- Compile una imagen de docker con un nginx  que contenga un index que muestre “hello nginx” 
- El workflow debe tener algún test de vulnerabilidades en la imagen. 
- La imagen debe ser alojada en algún repositorio externo a dockerHub o similar.  
- La imagen puede ser subida como  :latest    
- Adicionalmente puede usar semantic versioning para tener un histórico de compilaciones - (No requerido, pero será un plus) 




Dockerfile:

```dockerfile
# Usamos nginx:alpine como imagen base
FROM nginx:alpine

# Copiamos el nuevo index a su ruta
COPY index.html /usr/share/nginx/html

# exponemos el puerto http 
EXPOSE 80

# arrancamos nginx
CMD ["nginx", "-g", "daemon off;"]
```



Workflow Actions:

```yaml
name: Imagen Docker Prueba Tecnica

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  security-events: write
  actions: read
  contents: read
  
jobs:
  publicar-hello-nginx-docker-imagen:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - name: 'Checkout GitHub Action'
        uses: actions/checkout@main
      - name: 'Login to GitHub Container Registry'
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{github.actor}}
          password: ${{secrets.GITHUB_TOKEN}}
      - name: 'Build y Push'
        run: |
          docker build . --tag ghcr.io/manuelsysadmin/imagendockerpruebatecnica:latest
          docker push ghcr.io/manuelsysadmin/imagendockerpruebatecnica:latest
#Test de vulnerabilidad
  docker-scout:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
    - name: 'Login Docker'
      uses: docker/login-action@v3
      with:
        registry: docker.io
        username: ${{ secrets.DOCKERHUB_USER }}
        password: ${{ secrets.DOCKERHUB_PASS }}
    - name: Docker Scout CVEs
      uses: docker/scout-action@v0.18.1
      with:
        command: cves
        image: "ghcr.io/manuelsysadmin/imagendockerpruebatecnica:latest"
        only-fixed: true
        only-severities: critical,high
        write-comment: true
        github-token: ${{ secrets.GITHUB_TOKEN }} 
        exit-code: true
                     


```

### Resolución

**Todos los archivos estarán en el raíz del repositorio excepto el workflow que tendrá su ruta típica, se siguieron todas las indicaciones pedidas.** 

**El workflow se ejecutara cada vez que se realice un push al repositorio, realizará el build sobre el dockerfile usando el contenedor de nginx:alpine y además sobreescrivirá el archivo index.html del nginx por el requerido en la especificaciones. Por ultimo subirá la imagen al repositorio de github para contenedores y realizará el test de vulnerabilidades de docker scout.** 

## Playbook de ansible para deployar lo siguiente: 

- Instalar nginx (puede usar cualquier versión de familias .deb) 
- Configurar un index con jinja2 para que muestre el nombre del host donde está instalado en el index  (No requerido, pero será un plus)  
	**No quedó  claro el propósito del enunciado, por lo tanto el nombre del host se mostrará en el lanzamiento del playbook como en un archivo dentro de su maquina.**
- Adicionalmente debe justificar como resolver la problemática de aprovisionar 10 equipos con IP dinámica *           (No requerido, pero será un plus)   
    *  Como dato extra: ud sabe que han sido conectados a la red 192.168.100.0/24, pero cuya IP exacta no conoce, ya que han sido asignadas dinámicamente por un servidor DHCP.    

   **Asignamos un rango de ip en el inventario, en su ejecución pasará por todo el rango y lanzará el playbook a todas las maquinas que se pueda conectar.**
- Sabes que los equipos están en la misma red que el host desde el cual ejecutas Ansible. 
- No tienes acceso previo a sus direcciones IP. 
- Debes encontrar una forma de descubrir y gestionar estos equipos sin intervención manual directa en cada uno 

### Resolución
Todos los ficheros están en el raiz del repositorio:

**playbook.yml**: Jugadas para instalar Nginx y jinja2 requeridos.

**inventario.yml** : Inventario con el rango de ips para ejecutar los playbooks con la ruta de la clave ssh usada

**hostindex.j2**  : Jinja2 que muestra el hostname de la maquina

¿Cómo podrías adaptar el aprovisionamiento para que los equipos sean gestionables a pesar de que sus IP puedan cambiar en el futuro? 
**En el despliegue de los equipos o maquinas ya tendría configurado un usuario con los permisos necesarios , la clave ssh para la conexión desde la maquina ansible así pueda conectarse y ejecutar los playbooks correctamente.** 

Propón estrategias o herramientas para actualizar dinámicamente el inventory de Ansible en función de las IP asignadas por DHCP. 
**La estrategia mas básica es la seguida en esta prueba, se le asigna un rango de ip en el inventario y a cada host se le aplica el playbook. Una mejora sobre esto podría ser un script que generase un inventario dinámico sobre el rango de ip indicado y según el hostname de cada maquina lanzarle el playbook adecuado. Todo esto contando que los hostname tengan una convención ya preestablecida para poder asignarles grupos en el inventario por ejemplo: web01, web02, db01....**


## Develop
 Crear una API en python que resuelva lo siguiente: 

- Debe poder recibir via request HTTP un json (proporcionado debajo), parsearlo y devolver el valor de: hardware, event_A, traceID, publisher 

- El valor devuelto del parseado debe ser una pequeña tabla similar a lo siguiente 
- valor1: hardware 
- valor2: event_A 
- valor3: traceID 
- valor4: publisher 

 # Json de prueba. 

```json
{ "server": "demo01.server.com",
"environment": "production",
"hardware": "5.1.0",
"product": "SuperDuperDemo",
"MessageAtt": {
"event_type": {
"event_A": "String",
"value": "published"},
"traceID": "iddqdidkfa",
"intents": 0},
"Metadata": {
"host": "SuperDuperSimulator",
"origing": "onPrem",
"publisher": "demo-test",
"owner": "demo-user"}
}
```


**Para mostrar la tabla no me quedo claro como se quería por lo tanto se crean dos post distinto, uno devuelve la tabla en texto plano (/json_a_lista) y el otro en formato html (/json_a_tabla)**

Script Python pythonpruebatecnica.py.
```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/json_a_lista', methods=['POST'])
def json_a_lista():
    json_data = request.get_json()

    # Procesar el JSON para generar la tabla
    lista = "Valor 1:{}\n".format(json_data['hardware'])
    lista += "Valor 2:{}\n".format(json_data['MessageAtt']['event_type']['event_A'])
    lista += "Valor 3:{}\n".format(json_data['MessageAtt']['traceID'])
    lista += "Valor 4:{}\n".format(json_data['Metadata']['publisher'])


    return lista

@app.route('/json_a_tabla', methods=['POST'])
def json_a_tabla():
    json_data = request.get_json()

    # Procesar el JSON para generar la tabla
    html = "<table border='1'>"
    html += "<tr><th>Valor 1</th><td>{}</td></tr>".format(json_data['hardware'])
    html += "<tr><th>Valor 2</th><td>{}</td></tr>".format(json_data['MessageAtt']['event_type']['event_A'])
    html += "<tr><th>Valor 3</th><td>{}</td></tr>".format(json_data['MessageAtt']['traceID'])
    html += "<tr><th>Valor 4</th><td>{}</td></tr>".format(json_data['Metadata']['publisher'])
    html += "</table>"

    return html

if __name__ == '__main__':
    app.run(debug=True)

```

Curls para probar el script
```sh
#json_a_tabla html
curl -X POST -H "Content-Type: application/json" -d '{"server": "demo01.server.com", "environment": "production", "hardware": "5.1.0", "product": "SuperDuperDemo", "MessageAtt": {"event_type": {"event_A": "String", "value": "published"}, "traceID": "iddqdidkfa", "intents": 0}, "Metadata": {"host": "SuperDuperSimulator", "origing": "onPrem", "publisher": "demo-test", "owner": "demo-user"}}' http://localhost:5000/json_a_tabla
#json_a_lista texto plano
curl -X POST -H "Content-Type: application/json" -d '{"server": "demo01.server.com", "environment": "production", "hardware": "5.1.0", "product": "SuperDuperDemo", "MessageAtt": {"event_type": {"event_A": "String", "value": "published"}, "traceID": "iddqdidkfa", "intents": 0}, "Metadata": {"host": "SuperDuperSimulator", "origing": "onPrem", "publisher": "demo-test", "owner": "demo-user"}}' http://localhost:5000/json_a_lista
```


## Troubleshooting

Problemática:  

Ud recibe un escalado de ticket en el cual se comenta que al iniciar un servidor no existe un archivo (demo.tar.gz) que es utilizado para validar ciertas configuraciones del sistema.    
Quien escala el ticket comenta que este archivo es utilizado por dos aplicaciones, app01 y app02 pero que no sabe más al respecto.  

Troubleshoot realizado por nivel 1 

- Al conectarse al servidor encuentra que el archivo no existe, pero debería estar en "/opt/data/demo.tar.gz" 
- En los logs de sistema no encuentra nada relacionado a mv o rm asociado a demo.tar.gz 
- Tampoco encuentra información relevante en los logs de salida de las apps app01 y app02. 
- Se cree que un bug de alguna de las dos aplicaciones (app01 y/o app02) podría ser el causante de la pérdida del archivo. 
- El cliente le pide que justifique que aplicación o proceso es responsable de manipular este archivo.   

 Como información extra tiene lo siguiente: 

- Para resolver este incidente puede usar cualquier herramienta. 
- El usuario con el que se conecta al servidor tiene permisos de "sudo" y, debido a la criticidad del incidente, de ser necesario podría trabajar con "root" 
- Puede ver los procesos, llamadas de sistema y/o cualquier otra ingeniería necesaria llegar a dar con la posible causa. 
- El único equipo que tiene es el del problema, no puede replicar el escenario en otro entorno.    
    
¿Como podría abordar el trobuleshoot de este incidente? 

- Indique que razonamiento utilizaría. 
- Indique que herramientas utilizaría y por que. 
- Indique que y como analizaría.  (puede colocar los comandos que usaria)**

### Resolución:

Estos son pasos que se seguirían no necesariamente en ese orden, se actuaria según la experiencia que ya tenga en el sistema y con el aplicativo en concreto.

**Revisar los logs del sistema**: Aunque ya se han revisado los logs de sistema, es importante volver a revisarlos para buscar cualquier pista que pueda haberse pasado por alto.

**Buscar el archivo dentro del sistema** por si estuviera en una ruta distinta usando el comando find.

**Verificar la configuración de app1 y app2** : Revisar la configuración de ambas aplicaciones para ver si hay alguna referencia al archivo demo.tar.gz y confirmar que la ruta donde lo busca es la correcta. 

**Comprobar punto de montaje que lleva al a ruta del archivo**: Es posible que el montaje del disco o de red fallará y por eso las aplicaciones no encuentran el archivo en su ruta. Con ayuda del comando **mount** y del archivo de montaje **/etc/fstab** dictaminaremos si existe punto de montaje y si funciona correctamente.

**Mirar los permisos del archivo y su ruta**: Si localizamos el archivo comprobaremos que el usuario del aplicativo tiene los permisos necesarios para su manipulación. 

**Comprobar el espacio disponible en el punto de montaje que pertenece la ruta**, con **df -kh** como no dan datos de como funciona el archivo ni la aplicación puedo ponerme en la situación de que le archivo que falta sea consumible y es posible que en algún momento el disco se quedará sin espacio y no pueda cargar una nueva versión del archivo.
