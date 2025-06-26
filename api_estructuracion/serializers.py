from .models import *
from rest_framework import serializers
from drf_polymorphic.serializers import PolymorphicSerializer

############################ PEI  ##########################################
#Serializador Model PEI
class PeiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pei
        fields = '__all__'

#Serializador Model Objetivo PEI
class ObjetivoPeiSerializaer(serializers.ModelSerializer):
    class Meta:
        model = ObjetivoPei
        fields = '__all__'        

######################### SERIALIZADORES INDICADORES PEI #################################

#Serializador Indicador Cuantitativo PEI
class IndicadorPeiCuantitativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicadorPeiCuantitativo
        fields = '__all__'
        read_only_fields = ['creado_el', 'modificado_el', 'id', 'tipo']

#Serializador Indicador Cualitativo PEI
class IndicadorPeiCualitativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicadorPeiCualitativo
        fields = '__all__'
        read_only_fields = ['creado_el', 'modificado_el', 'id', 'tipo']

class IndicadorPeiBaseSerializer(serializers.ModelSerializer):
    tipo_detalle = serializers.SerializerMethodField()
    tipo = serializers.CharField(write_only=True, required=True)  

    class Meta:
        model = IndicadorPeiBase
        fields = '__all__'

    def get_tipo_detalle(self, obj):
        if isinstance(obj, IndicadorPeiCuantitativo):
            return IndicadorPeiCuantitativoSerializer(obj).data
        elif isinstance(obj, IndicadorPeiCualitativo):
            return IndicadorPeiCualitativoSerializer(obj).data
        return None
    
    def create(self, validated_data):
        tipo = validated_data.pop('tipo')
        
        if tipo == 'Proporcion':
            return IndicadorPeiCuantitativo.objects.create(**validated_data)
        elif tipo == 'Avance':
            return IndicadorPeiCualitativo.objects.create(**validated_data)
        else:
            raise serializers.ValidationError("Tipo de indicador no válido")
        
##################### SERIALIZADORES Objetivos - Indicadores      #############################

# Serializador base polimórfico para indicadores
class IndicadorPeiPolymorphicSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        if isinstance(instance, IndicadorPeiCuantitativo):
            return IndicadorPeiCuantitativoSerializer(instance, context=self.context).data
        elif isinstance(instance, IndicadorPeiCualitativo):
            return IndicadorPeiCualitativoSerializer(instance, context=self.context).data
        return super().to_representation(instance)
    
    class Meta:
        model = IndicadorPeiBase
        fields = '__all__'

# Serializador para objetivos con sus indicadores
class ObjetivoPeiSerializer(serializers.ModelSerializer):
    indicadores = serializers.SerializerMethodField()
    
    class Meta:
        model = ObjetivoPei
        fields = ['id', 'codigo', 'descripcion', 'creado_el', 'modificado_el', 'indicadores']
    
    def get_indicadores(self, obj):
        # Obtener todos los indicadores relacionados con este objetivo
        indicadores = obj.indicador_pei_objetivo.all()
        return IndicadorPeiPolymorphicSerializer(indicadores, many=True).data

# Serializador para el PEI con sus objetivos
class PeiObjetivosSerializer(serializers.ModelSerializer):
    objetivos = ObjetivoPeiSerializer(many=True, read_only=True, source='pei_obj_general')
    
    class Meta:
        model = Pei
        fields = ['id', 'titulo', 'objetivos']

        
############################# PROYECTO #######################################
##MODELOS
#Serializador Model Proyecto
class ProyectoDatosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'

    def create(self, validated_data):
        instancia_gestora_data = validated_data.pop('instancia_gestora', [])
        # Crear proyecto sin el campo M2M
        proyecto = Proyecto.objects.create(**validated_data)
        # Asignar M2M después
        if instancia_gestora_data:
            proyecto.instancia_gestora.set(instancia_gestora_data)

        # Crear nodo para DiagramaEstructura con info actualizada
        nodo = {
            "id": "1",
            "type": "proyecto",
            "dimensions": {
                "width": 500,
                "height": 445
            },
            "computedPosition": {"x": 0, "y": 0, "z": 0},
            "handleBounds": {
                "source": [{
                    "id": "source-1",
                    "type": "source",
                    "nodeId": "1",
                    "position": "bottom",
                    "x": 244,
                    "y": 439.0625,
                    "width": 12,
                    "height": 12
                }],
                "target": None
            },
            "selected": False,
            "dragging": False,
            "resizing": False,
            "initialized": False,
            "isParent": False,
            "position": {"x": 0, "y": 0},
            "data": {
                "label": "Proyecto",
                "type": "proyecto",
                "estado": proyecto.estado,
                "datosNodo": {
                    "id": proyecto.id,
                    "codigo": proyecto.codigo,
                    "titulo": proyecto.titulo,
                    "descripcion": proyecto.descripcion,
                    "fecha_creacion": proyecto.fecha_creacion.isoformat() if proyecto.fecha_creacion else None,
                    "fecha_inicio": proyecto.fecha_inicio.isoformat() if proyecto.fecha_inicio else None,
                    "fecha_finalizacion": proyecto.fecha_finalizacion.isoformat() if proyecto.fecha_finalizacion else None,
                    "presupuesto": str(proyecto.presupuesto),
                    "estado": proyecto.estado,
                    "creado_por": str(proyecto.creado_por),
                    "pei": proyecto.pei_id,
                    "instancia_gestora": list(proyecto.instancia_gestora.values_list('id', flat=True))
                }
            },
            "events": {}
        }

        DiagramaEstructura.objects.create(
            proyecto=proyecto,
            codigoProyecto=proyecto.codigo,
            nodos=[nodo],
            conexiones=[]
        )

        return proyecto
        

#Serializador de un proyecto
class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'


#Serializador MOdel Objetivo General
class ProyObjGralSer(serializers.ModelSerializer):
    class Meta:
        model = ObjetivoGeneralProyecto
        fields = '__all__'        

#serializador MOdel Objetivo especifico
class ProyObjEspSer(serializers.ModelSerializer):
    class Meta:
        model = ObjetivoEspecificoProyecto
        fields = '__all__'        

#Serializador Model Kpi
class KpiSer(serializers.ModelSerializer):
    class Meta:
        model = Kpi
        fields = '__all__'

#Serializador Model: Instancia Gestora
class ProyInsGestSer(serializers.ModelSerializer):
    class Meta:
        model = InstanciaGestora
        fields = '__all__'     


#Serializador Model: ProcedenciaFondos
class ProcedenciaFondosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedenciaFondos
        fields = '__all__'     

#Serializador Model: DiagramaEstructura
class DiagramaEstructuraSer(serializers.ModelSerializer):
    class Meta:
        model = DiagramaEstructura
        fields = '__all__'

#Serializador Actualizar los nodos y edges
class DiagramaEstructuraUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagramaEstructura
        fields = ['nodos', 'conexiones']

##NO MODELOS
#Solo proyectos en estado de Planificacion
class ProyectoPlanificacionSerializer(serializers.ModelSerializer):
    instancia_gestora = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Proyecto
        fields = [
            'id', 'codigo', 'titulo', 'descripcion',
            'fecha_creacion', 'fecha_inicio', 'fecha_finalizacion',
            'presupuesto', 'estado', 'creado_por', 'pei', 'instancia_gestora'
        ]

#Proyecto - estructura -serializador
class InstanciaGestoraSer(serializers.ModelSerializer):
    class Meta:
        model = InstanciaGestora
        fields = ['codigo', 'clasificador', 'instancia']

class ProyectoEstructuraSer(serializers.ModelSerializer):
    mapa_nodo = DiagramaEstructuraSer(read_only=True)
    instancia_gestora = InstanciaGestoraSer(many=True, read_only = True)
    class Meta:
        model = Proyecto
        fields = ['id', 'codigo', 'titulo', 'descripcion', 'estado', 'fecha_creacion',
                  'fecha_inicio', 'fecha_finalizacion', 'presupuesto', 'pei',
                  'instancia_gestora', 'creado_por', 'mapa_nodo']


#Serializador para el Indicador de Objetivo Especifico
class IndicadorObjetivoGralSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicadorObjetivoGeneral
        fields = '__all__'

#Serializador para el Resultado de Objetivo General
class ResultadoOGSerializaer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoOG
        fields = '__all__'

#Serializador Resultado Objetivo Especifico
class ResultadoOESer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoOE
        fields = '__all__'

#Serializador Producto Objetivo Especifico
class ProductoOESer(serializers.ModelSerializer):
    class Meta:
        model = ProductoOE
        fields = '__all__'        

#Serializador para el Indicador de Resultado de Objetivo General
class IndicadorResultadoObjGralSerializ(serializers.ModelSerializer):
    class Meta:
        model = IndicadorResultadoObjGral
        fields = '__all__'        

#Serializador para Indicador de Objetivo Especifico OG
class IndicadorObjetivoEspecificoSer(serializers.ModelSerializer):
    class Meta:
        model = IndicadorObjetivoEspecifico
        fields = '__all__'

#Serializador Indicador Resultado OE
class IndicadorResultadoOESer(serializers.ModelSerializer):
    class Meta:
        model = IndicadorResultadoObjEspecifico
        fields = '__all__'

#Serializador Producto Resultado OE
class ProductoResultadoOESer(serializers.ModelSerializer):
    class Meta:
        model = ProductoResultadoOE
        fields = '__all__'

#Serializador para el Producto General
class ProductoGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoGeneral
        fields = '__all__'

#Serializador Proceso
class ProcesosSerializador(serializers.ModelSerializer):
    class Meta:
        model = Proceso
        fields = '__all__'      


#Serializador Actividad
class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = '__all__'

############################################## ESTRUCTURA COMPLETA DEL PROYECTO   #####################################################
#Procesos serializador
class ProcesosSer(serializers.ModelSerializer):
    class Meta:
        model = Proceso
        fields = '__all__'


#Actividades Serializado
class ActividadesSer(serializers.ModelSerializer):

    class Meta:
        model = Actividad
        fields = '__all__'


class ProcesoActividadSerializer(serializers.ModelSerializer):
    actividades = ActividadesSer(many=True, source='actividad_proceso')
    
    class Meta:
        model = Proceso
        fields = '__all__'


# Indicador de Objetivo General
class IndicadorObjetivoGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicadorObjetivoGeneral
        fields = ['id', 'codigo', 'redaccion', 'baseline', 'target_q1', 'target_q2', 'target_q3', 'target_q4', 'objetivo_general']

# KPI de Objetivo General
class KpiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kpi
        fields = ['id', 'codigo', 'descripcion']

# Indicador de Resultado Objetivo General
class IndicadorResultadoObjetivoGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicadorResultadoObjGral
        fields = ['id', 'codigo', 'redaccion']

#Resultado de Objetivo General junto con Indicator
class ResultadoObjetivoGeneralSerializer(serializers.ModelSerializer):
    indicador_res_objgral = IndicadorResultadoObjetivoGeneralSerializer(many=True, source='indicador_res_og', read_only=True)
    procesos_res_objgral = ProcesoActividadSerializer(source='proceso_resultado_og')
    actividades_res_objgral = ActividadesSer(many=True, source='actividad_resultado_og', read_only=True)

    class Meta:
        model = ResultadoOG
        fields = ['id', 'codigo', 'descripcion', 'indicador_res_objgral', 'procesos_res_objgral', 'actividades_res_objgral']


#Indicador Resultado Objetivo Especifico
class IndicadorResultadoObjetivoEspecificoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicadorResultadoObjEspecifico
        fields = '__all__'


#Producto de Resultado Objetivo Especifico
class ProductoResObjEspecificoSer(serializers.ModelSerializer):
    class Meta:
        model = ProductoResultadoOE
        fields = '__all__'


#Resultado de Objetivo Especifico
class ResultadoObjetivoEspecificoSerializer(serializers.ModelSerializer):
    #Indicador de Resultado OE
    indicadores_resultado_objesp = IndicadorResultadoObjetivoEspecificoSerializer(many=True, source='indicador_res_oe', read_only=True)
    #Producto de Resultado OE
    productos_resultado_objesp = ProductoResObjEspecificoSer(many=True, source='productos_res_oe', read_only=True) 
    #Proceso para Resultado OE
    proceso_resultado_objesp = ProcesoActividadSerializer(many=False, source='proceso_resultado_oe', read_only=True)
    #Actividad para Resultado OE
    actividades_resultado_objesp = ActividadesSer(many=True, source="actividad_resultado_oe", read_only=True )
    
    class Meta:
        model = ResultadoOE
        fields = '__all__'


#Productos de Objetivo Especifico
class ProductosOeSeria(serializers.ModelSerializer):
    proceso_producto_objesp = ProcesoActividadSerializer(many=False, source='proceso_producto_oe', read_only=True)
    actividades_producto_objesp = ActividadesSer(many=True, source='actividad_producto_oe', read_only=True)
    class Meta:
        model = ProductoOE
        fields = '__all__'

#Indicador de Objetivo Especifico
class IndicadorOESeria(serializers.ModelSerializer):
    class Meta:
        model = IndicadorObjetivoEspecifico
        fields = '__all__'


#Objetivo Especifico
class ObjetivoEspecificoSeria(serializers.ModelSerializer):
    #Indicador Objetivo Especifico
    indicadores_objesp = IndicadorOESeria(many=True, source='indicador_oe', read_only= True)
    #Producto de Objetivo Especifico
    productos_objesp = ProductosOeSeria(many=True, source='productos_oe', read_only=True)
    #Resultado de Objetivo Especifico
    resultado_objesp = ResultadoObjetivoEspecificoSerializer(many=True, source='resultados_oe', read_only=True)
    class Meta:
        model = ObjetivoEspecificoProyecto
        fields = '__all__' 


# Objetivo General junto con kpi, indicador, resultado
class ObjetivoGeneralSerializer(serializers.ModelSerializer):
    kpi = KpiSerializer(many=True, source='kpis', read_only=True)
    indicadores_objgral = IndicadorObjetivoGeneralSerializer(many=True, source='indicador_og', read_only=True)
    resultados_objgral = ResultadoObjetivoGeneralSerializer(many=True, source='resultados_og', read_only=True)
    #Objetivo Especifico relacionado al Objetivo General
    objetivos_especificos = ObjetivoEspecificoSeria(many=True, source='objetivos_especificos_og', read_only=True)

    class Meta:
        model = ObjetivoGeneralProyecto
        fields = ['id', 'codigo', 'descripcion', 'kpi', 'indicadores_objgral', 'resultados_objgral', 'objetivos_especificos']

# Estrcutura del proyecto
class ProyectoEstructuraSerializer(serializers.ModelSerializer):
    objetivo_general = ObjetivoGeneralSerializer()
    objetivo_especifico = ObjetivoEspecificoSeria(many=True, source='objetivos_especificos', read_only=True)

    class Meta:
        model = Proyecto
        fields = ['id', 'codigo', 'titulo', 'descripcion', 'objetivo_general', 'objetivo_especifico']

############################################## FIN ESTRUCTURA COMPLETA DEL PROYECTO   #####################################################


