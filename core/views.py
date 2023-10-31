from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.hashers import  check_password
from core.models import Cliente, Productos, Pedido, Categoria
from django.views import  View
  
# Create your views here.

def index(request):
       return render(request, 'base.html')

class Carrito(View):
    def get(self , request):
        ids = list(request.session.get('carrito').keys())
        productos = Productos.get_productos_por_id(ids)
        print(productos)
        return render(request , 'carrito.html' , {'productos' : productos} )
    

class CheckOut(View):
    def post(self, request):
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        cliente = request.session.get('cliente')
        carrito = request.session.get('carrito')
        productos = Productos.get_productos_por_id(list(carrito.keys()))
        print(direccion, telefono, cliente, carrito, productos)
  
        for producto in productos:
            print(carrito.get(str(producto.id)))
            pedido = Pedido(cliente=Cliente(id=cliente),
                          producto=producto,
                          precio=producto.precio,
                          direccion=direccion,
                          telefono=telefono,
                          cantidad=carrito.get(str(producto.id)))
            pedido.save()
        request.session['carrito'] = {}
  
        return redirect('carrito')
    

class Index(View):
  
    def post(self, request):
        producto = request.POST.get('producto')
        quitar = request.POST.get('quitar')
        carrito = request.session.get('carrito')
        if carrito:
            cantidad = carrito.get(producto)
            if cantidad:
                if quitar:
                    if cantidad <= 1:
                        carrito.pop(producto)
                    else:
                        carrito[producto] = cantidad-1
                else:
                    carrito[producto] = cantidad+1
  
            else:
                carrito[producto] = 1
        else:
            carrito = {}
            carrito[producto] = 1
  
        request.session['carrito'] = carrito
        print('carrito', request.session['carrito'])
        return redirect('homepage')
  
    def get(self, request):
        # print()
        return HttpResponseRedirect(f'/core{request.get_full_path()[1:]}')
  
  
def core(request):
    carrito = request.session.get('carrito')
    if not carrito:
        request.session['carrito'] = {}
    productos = None
    categorias = Categoria.get_todas_las_categorias()
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = Productos.get_todos_los_productos_por_categoria_id(categoria_id)
    else:
        productos = Productos.get_todos_los_productos()
  
    data = {}
    data['productos'] = productos
    data['categorias'] = categorias
  
    print('Sos : ', request.session.get('email'))
    return render(request, 'index.html', data)

class Login(View):
    return_url = None
  
    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')
  
    def post(self, request):
        email = request.POST.get('email')
        contraseña = request.POST.get('contraseña')
        cliente = cliente.get_cliente_por_email(email)
        error_message = None
        if cliente:
            flag = check_password(contraseña, cliente.contraseña)
            if flag:
                request.session['cliente'] = cliente.id
  
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('home')
            else:
                error_message = 'No es válido'
        else:
            error_message = 'No es válido'
  
        print(email, contraseña)
        return render(request, 'login.html', {'error': error_message})
  
  
def logout(request):
    request.session.clear()
    return redirect('login')

class Pedido(View):
  
    def get(self, request):
        cliente = request.session.get('cliente')
        pedidos = Pedido.get_pedidos_de_Cliente(cliente)
        print(pedidos)
        return render(request, 'pedidos.html', {'pedidos': pedidos})


class Registrarse (View):
    def get(self, request):
        return render(request, 'registrarse.html')
  
    def post(self, request):
        postData = request.POST
        nombre = postData.get('nombre')
        apellido = postData.get('apellido')
        telefono = postData.get('telefono')
        email = postData.get('email')
        contraseña = postData.get('contraseña')
        # validacion
        value = {
            'nombre': nombre,
            'apellido': apellido,
            'telefono': telefono,
            'email': email
        }
        mensaje_de_error = None
  
        cliente = Cliente(nombre=nombre,
                            apellido=apellido,
                            telefono=telefono,
                            email=email,
                            contraseña=contraseña)
        mensaje_de_error = self.validarCliente(cliente)
  
        if not mensaje_de_error:
            print(nombre, apellido, telefono, email, contraseña)
            cliente.contraseña = contraseña(cliente.contraseña)
            cliente.registrar()
            return redirect('homepage')
        else:
            data = {
                'error': mensaje_de_error,
                'values': value
            }
            return render(request, 'registrarse.html', data)
  
    def validarCliente(self, cliente):
        mensaje_de_error = None
        if (not cliente.nombre):
            mensaje_de_error = "Por favor, ingrese su nombre"
        elif len(cliente.nombre) < 3:
            mensaje_de_error = 'El nombre debe tener mínimo 3 caracteres'
        elif not cliente.apellido:
            mensaje_de_error = 'Por favor, ingrese su apellido'
        elif len(cliente.apellido) < 3:
            mensaje_de_error = 'El apellido debe tener mínimo 3 caracteres'
        elif not cliente.telefono:
            mensaje_de_error = 'Ingrese su número de teléfono'
        elif len(cliente.telefono) < 8:
            mensaje_de_error = 'El númeno de teléfono debe tener mínimo 8 caracteres'
        elif len(cliente.contraseña)  < 5:
            mensaje_de_error = 'La contraseña debe tener mínimo 5 caracteres'
        elif len(cliente.email) < 5:
            mensaje_de_error = 'El email debe tener mínimo 5 caracteres'
        elif cliente.Existe():
            mensaje_de_error = 'La dirección de email ya está registrada'
        # guardar
  
        return mensaje_de_error
    


