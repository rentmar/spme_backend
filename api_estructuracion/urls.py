from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

#PEI
router = DefaultRouter()
#PEI
router.register(r'pei', PeiViewModel, basename='pei')
router.register(r'indicadores', IndicadorPeiViewSet, basename='indicadores')
router.register(r'objetivos-pei', ObjetivosPeiViewModel, basename='obj.pei')
router.register(r'indicadores-cuantitativos', IndicadorPeiCuantitativoViewSet)
router.register(r'indicadores-cualitativos', IndicadorPeiCualitativoViewSet)



#PROYECTOS
router.register(r'proyectos', ProyectoViewModel, basename='proyectos')
#Proyectos - Diagrama
router.register(r'diagramas', DiagramaEstructuraView, basename='diagrama_proyecto')
#Proyectos - Objetivo General
router.register(r'proy-obj-gral', ProyObjGralViewModel , basename='proy_obj_gral')
router.register(r'proy-obj-esp', ProyObjEspViewModel, basename='proy_obj_esp')
router.register(r'kpi', KpiViewSet, basename='kpi_proyecto')
router.register(r'instancia-gestora', ProyInstGestoraViewModel, basename='inst_gestora')
router.register(r'indicadores-og', IndicadorObjetivoGralViewset, basename='indicador_obj_gral')
router.register(r'indicador-oe', IndicadorObjetivoEspecificoViewset, basename="indicador_obj_espec")
router.register(r'indicador-resultado-oe', IndicadorResultadoOEViewset, basename='indicador_resultado_oe')
router.register(r'indicador-resultado-og', IndicadorResultadoOgViewset, basename="indicador_resultado_obj_gral")
router.register(r'resultado-og', ResultadoObjetivoGeneralViewset, basename="resultado_obj_gral")
router.register(r'resultado-oe', ResultadoObjetivoEspecificoViewset, basename="resultado_obj_espec")
router.register(r'producto-oe', ProductoOEViewset, basename='producto_obj_espec')
router.register(r'producto-result-oe', ProductoResultadoOEViewset, basename='producto_res_oe')
router.register(r'producto-general', ProductoGeneralViewset, basename='producto_general')
router.register(r'procesos', ProcesoViewset, basename='procesos')
router.register(r'actividades', ActividadViewset, basename='actividades')
router.register(r'procedencia-fondos', ProcedenciaFondosViewmodel, basename='procedencia_fondos')
#Indicadores del objetivo

#router.register(r'indicadores-numericos', IndicadorNumericoViewSet, basename='indicador-numerico')
#router.register(r'indicadores-literales', IndicadorLiteralViewSet, basename='indicadores-literales')
#router.register(r'indicadores-porcentuales', IndicadorPorcentualViewSet, basename='indicadores-porcentuales')
#router.register(r'proyectos-completos', ProyectoCompletoView, basename='proyectos-completos') #Proyecto, con obj general e info relacionada

#OBJETIVOS ESPECIFICOS
#router.register(r'objetivos-especificos', ObjetivoEspecificoProyectoViewSet)
#router.register(r'indicadores-especificos', IndicadorObjEspecProyViewSet)
#router.register(r'resultados', ResultadoObjEspProyViewSet)
#router.register(r'indicadores-resultados', IndicadorResultadoProyViewSet)
#router.register(r'actividades', ActividadBaseResultadoViewSet)
#router.register(r'lineas-accion', LineaAccionResultadoViewSet)


# URL patterns adicionales que no son ViewSets
urlpatterns = [
    #path(r'proy-detalle/<int:pk>/', ProyectoDetalleView.as_view(), name='proy_detalle'),
    #path(r'proyecto-objesp-info/<int:id>/', ProyectoCompletoDetailView.as_view(), name='proyecto-obj-info'),
    path(r'pei/<int:pk>/objetivos/', PeiObjetivosIndicadoresView.as_view(), name='pei-objetivos'),
    path(r'pei-vigente/', obtener_pei_vigente, name='pei-vigente'),
    path(r'pei-vigente/<int:pei_id>/', establecer_pei_vigente, name='establecer-pei-vigente'),
    path(r'proyectos/planificacion/<int:pei_id>/', ProyectoPlanificacionView.as_view(), name='proyectos-planificacion'  ),
    path(r'proyectos/<int:proyecto_id>/objetivo-general/', ObjetivoGeneralPorProyectoView.as_view(), name='obj-general-por-proyecto'),
    path(r'proyecto-estructura-nodos/<int:id>/', ProyectoEstructuraView.as_view(), name='proyecto-estructura' ),
    path(r'diagramas/<int:pk>/actualizar/', DiagramaEstructuraUpdateView.as_view(), name='actualizar-diagrama'),
    path(r'proyecto/<int:pk>/estructura/', ProyectoDetalladoView.as_view(), name='proyecto-id-estructura' ),
    path(r'proyectos-planificacion/', ProyectosPlanificacionList.as_view(), name='proyecto-planificacion' ),
    path(r'test/', test_endpoint, name='test-endpoint'),    
]

urlpatterns += router.urls