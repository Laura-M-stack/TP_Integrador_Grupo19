from django.db import models
import datetime


# Create your models here.
class Categoria:
    name = models.CharField(max_length=50)
  
    @staticmethod
    def get_todas_las_categorias():
        return Categoria.objects.all()
  
    def __str__(self):
        return self.name
    

class Cliente:
      
      def __init__(self, nombre, apellido, telefono, email, contraseña):   
        nombre = models.CharField(max_length=50)
        apellido = models.CharField(max_length=50)
        telefono = models.CharField(max_length=10)
        email = models.EmailField()
        contraseña = models.CharField(max_length=100)
  
    # para guardar datos
      def registrar(self):
        self.save()
  
      @staticmethod
      def get_cliente_por_email(email):
        try:
            return cliente.objects.get(email=email)
        except:
            return False
  
      def Existe(self):
        if cliente.objects.filter(email=self.email):
            return True
  
        return False
    

class Pedido:
      
      def __init__(self, producto, cliente, cantidad, precio, direccion, telefono, fecha, estado):
        producto = models.ForeignKey(productos,
                                on_delete=models.CASCADE)
        cliente = models.ForeignKey(cliente,
                                 on_delete=models.CASCADE)
        cantidad = models.IntegerField(default=1)
        precio = models.IntegerField()
        direccion = models.CharField(max_length=50, default='', blank=True)
        telefono = models.CharField(max_length=50, default='', blank=True)
        fecha = models.DateField(default=datetime.datetime.today)
        estado = models.BooleanField(default=False)
  
      def realizar_pedido(self):
        self.save()
  
      @staticmethod
      def get_pedidos_de_cliente(cliente_id):
        return pedido.objects.filter(cliente=cliente_id).order_by('-date')
    

class Productos:
      
      def __init__(self, nombre, precio, categoria, descripcion, imagen):
        nombre = models.CharField(max_length=60)
        precio = models.IntegerField(default=0)
        categoria = models.ForeignKey(categoria, on_delete=models.CASCADE, default=1)
        descripcion = models.CharField(
          max_length=250, default='', blank=True, null=True)
        imagen = models.ImageField(upload_to='uploads/productos/')
  
      @staticmethod
      def get_productos_por_id(ids):
        return productos.objects.filter(id__in=ids)
  
      @staticmethod
      def get_todos_los_productos():
        return productos.objects.all()
  
      @staticmethod
      def get_todos_los_productos_por_categoria_id(categoria_id):
        if categoria_id:
            return productos.objects.filter(categoria=categoria_id)
        else: productos.get_todos_los_productos()