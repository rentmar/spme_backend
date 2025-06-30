from django.contrib import admin
from .models import *
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin


#Pei
admin.site.register(Pei)
admin.site.register(ObjetivoPei)
admin.site.register(FactoresCriticos)

@admin.register(IndicadorPeiBase)
class IndicadorAdmin(PolymorphicParentModelAdmin):
    base_model = IndicadorPeiBase
    child_models = (IndicadorPeiCualitativo, IndicadorPeiCuantitativo)


@admin.register(IndicadorPeiCuantitativo)
class IndicadorPeiCuantitativoAdmin(PolymorphicChildModelAdmin):
    base_model = IndicadorPeiBase

@admin.register(IndicadorPeiCualitativo)
class IndicadorPeiCualitativoAdmin(PolymorphicChildModelAdmin):
    base_model = IndicadorPeiBase


#Proyectos
admin.site.register(InstanciaGestora)
admin.site.register(Proyecto)
admin.site.register(ObjetivoGeneralProyecto)
admin.site.register(Kpi)
admin.site.register(ObjetivoEspecificoProyecto)
admin.site.register(Proceso)
admin.site.register(DiagramaEstructura)
admin.site.register(ResultadoOG)
admin.site.register(ResultadoOE)
admin.site.register(ProductoOE)
admin.site.register(ProductoResultadoOE)
admin.site.register(ProductoGeneral)
admin.site.register(Actividad)
admin.site.register(ProcedenciaFondos)

#INdicador de Objetivo Especifico
@admin.register(IndicadorProyecto)
class IndicadorProyectoAdmin(PolymorphicParentModelAdmin):
    base_model = IndicadorProyecto
    child_models = (IndicadorObjetivoGeneral, 
                    IndicadorResultadoObjGral,
                    IndicadorObjetivoEspecifico,
                    IndicadorResultadoObjEspecifico
                    )
    list_display = ('id', 'codigo')
    

@admin.register(IndicadorObjetivoGeneral)
class IndicadorObjetivoGeneralAdmin(PolymorphicChildModelAdmin):
    base_model=IndicadorProyecto

@admin.register(IndicadorResultadoObjGral)
class IndicadorResultadoObjGralAdmin(PolymorphicChildModelAdmin):
    base_model=IndicadorProyecto

@admin.register(IndicadorObjetivoEspecifico)
class IndicadorObjetivoEspecificoAdmin(PolymorphicChildModelAdmin):
    base_model=IndicadorProyecto    

@admin.register(IndicadorResultadoObjEspecifico)
class IndicadorResultadoObjEspecificoAdmin(PolymorphicChildModelAdmin):
    base_model=IndicadorProyecto


    