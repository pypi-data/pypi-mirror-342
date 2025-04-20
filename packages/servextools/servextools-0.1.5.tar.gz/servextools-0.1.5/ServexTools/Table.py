import time
import ServexTools.Tools as Tools
from ServexTools.socket_manager import get_socketio
import typing as t
from io import StringIO
from functools import lru_cache

COLUMNA = "NombreColumnas"
DATO = "DatosColumnas"
CLASS = "ClassColumnas"
FORMATO = "ColumnasFormato"
TOTALIZAR = "ColumnasTotalizar"
SUBDATOS = "SubColumnasDatos"
FORMAT_HANDLERS = {
    'dict': lambda x, key: x[key],
    'list': lambda x, key: next((item[key] for item in x), None)
}
socketio = get_socketio()
def CrearTabla(Datos: t.Union[list, list],
               NombreColumnas: t.Union[tuple, tuple] = None,
               DatosColumnas: t.Union[tuple, tuple] = None,
               ClassColumnas: t.Union[tuple, tuple] = None,
               FormatoColumnas: t.Union[tuple, bool] = False,
               TotalizarColumnas: t.Union[tuple, bool] = False,
               ColumnasJson: t.Union[list, dict] = None,
               SubColumnasDatos: t.Union[list, bool] = False,
               SubFilas: t.Union[list, bool] = False,
               FilasPlus: t.Union[list, bool] = False,
               MarcarRows:t.Union[tuple, bool] = False,
               Titulo="Detalle",
               nombreClase='TablaFilas',
               idtable="table", paginacion=False, MostrarLosTH=False, MostralConteo=True, TablaNumero=0, IncluirScript=True, RealizarReplace=False,LongitudPaginacion=200,claseprincipal="AlturaGrid",progressBar=False,sessionidusuario=None,reporte=False,conteo=True):
    r"""
[Github con la explicacion](https://github.com/Servextex/documentaciones/blob/main/table.md)
    """

    # Si se proporciona ColumnasJson, convertir al formato anterior
    if ColumnasJson:
        NombreColumnas = tuple(col[COLUMNA] for col in ColumnasJson)
        DatosColumnas = tuple(col[DATO] for col in ColumnasJson)
        ClassColumnas = tuple(col.get(CLASS, "") for col in ColumnasJson)
        FormatoColumnas = tuple(col.get(FORMATO, "") for col in ColumnasJson)
        TotalizarColumnas = tuple(col.get(TOTALIZAR, False) for col in ColumnasJson)
        SubColumnasDatos = tuple(col.get(SUBDATOS, False) for col in ColumnasJson)

    ValidarLongitudDatos(NombreColumnas, DatosColumnas, ClassColumnas, FormatoColumnas, TotalizarColumnas, SubColumnasDatos)
    try:
        if progressBar==True:
            tamano_datos = len(Datos)
    except Exception as e:
        pass

    countCol = 0
    ColumnasTH = StringIO()
    Totales = {}
    for col in NombreColumnas:
        ColumnasTH.write(f'<th scope="col" class="{ClassColumnas[countCol]}">{col}</th>')
        countCol += 1

    countCol = 0
    if TotalizarColumnas and not isinstance(TotalizarColumnas, bool) and any(TotalizarColumnas):
        for col in DatosColumnas:
            Totalizar = TotalizarColumnas[countCol]
            if Totalizar == True:
                Totales.update({
                    'T'+col: 0.00
                })
            countCol += 1

    countCol = 0
    countFilas = 0
    emitirEnD = 0
    ColumnasTD = StringIO()
    FilasTD = StringIO()
    if Datos == [] or Datos is None:
        if MostrarLosTH == False:
            ColumnasTH = StringIO()
            FilasTD = StringIO()
            FilasTD.write("<div class='text-center'>NO SE ENCONTRARON DATOS.</div>")
    else:
        # Precalcular valores comunes
        class_map = {i: ClassColumnas[i] for i in range(len(ClassColumnas))}
        format_map = {i: FormatoColumnas[i] for i in range(len(FormatoColumnas))} if FormatoColumnas else {}
        
        for row in Datos:
            if RealizarReplace:
                row = {k: v.replace("\n", "<stln>") if isinstance(v, str) and "\n" in v else v 
                      for k, v in row.items()}

            NumeralTabla = str(countFilas)+str(TablaNumero) if TablaNumero > 0 else str(countFilas)
            style="background-color: #97d2ea;" if SubFilas != False else ""
            if MarcarRows != False:
                Respuesta=MarcarFilas(MarcarRows,SubColumnasDatos,DatosColumnas,row)
                FilasTD.write(CrearFila(nombreClase, NumeralTabla, style, Respuesta))
            else:
                FilasTD.write(f"<tr id='rows_{NumeralTabla}' class='{nombreClase} CursorPointer' style='{style}'>")

            countFilas += 1
            for i, col in enumerate(DatosColumnas):
                columna = ProcesarSubDatos(SubColumnasDatos, i, col, row)
                if format_map:
                    columna = Formatos(FormatoColumnas, i, columna)

                if TotalizarColumnas and not isinstance(TotalizarColumnas, bool) and any(TotalizarColumnas):
                    Sumar = TotalizarColumnas[i]
                    if Sumar == True:
                        Totales['T'+str(col)] += Tools.StrToFloat(columna)

                ColumnasTD.write(f'<td id="{col}_{NumeralTabla}" class="{class_map[i]} text-wrap">{columna}</td>')

            if SubFilas != False:
                FilasTD.write(ColumnasTD.getvalue())
                #Dt, NombColumnas, DtColumnas, FrtColumnas=ProcesarSub(SubFilas, row)
                # DtSubFilas = HtmlSubfilas(Datos=Dt, NombreColumnas=NombColumnas, DatosColumnas=DtColumnas, FormatoColumnas=FrtColumnas,FilasPlus=FilasPlus)
                DtSubFilas=ProcesarSubFilas(SubFilas=SubFilas, row=row,FilasPlus=FilasPlus)
                FilasTD.write(DtSubFilas)
                FilasTD.write("</tr>")
            else:
                FilasTD.write(ColumnasTD.getvalue())
                FilasTD.write("</tr>")

            ColumnasTD = StringIO()
            countCol = 0
            emitirEnD+=1
            if progressBar == True and emitirEnD>=350:
                socketio.emit(f"ProgresoDeTablaReport_{sessionidusuario}", {'transcurrido': countFilas, 'total': tamano_datos, 'barra': True})
                time.sleep(0.5)
                emitirEnD=0

    ScriptPaginacion = ""
    if paginacion == True and Datos != [] and countFilas>=LongitudPaginacion:
        # ScriptPaginacion = """
        #     $(function () {  
        #             $.fn.dataTable.ext.errMode = 'none';
        #             $("#"""+idtable+"""").DataTable({
        #                 ordering: false,
        #                 searching: false,
        #                 info: false,
        #                 select: true,
        #                 lengthChange: false,
        #                 pageLength: """+str(LongitudPaginacion)+""",
        #                 language: {
        #                     paginate: {
        #                         previous: '‹',
        #                         next:     '›'
        #                     }
        #                 }
        #             });  
        #     setTimeout(function () {
        #         $('#"""+idtable+"""').removeAttr('style');
        #     }, 1000);
        #             });  
        # """
        ScriptPaginacion = """
            $(function () {  
                    paginateTable('"""+idtable+"""', """+str(LongitudPaginacion)+""");
                    });  
        """
    Script = ""
    if IncluirScript == True:
        Script = """
                <script>
             
            function """+idtable+"""(callback) {
                try {
                    var elementos = document.querySelectorAll('."""+nombreClase+"""');

                    elementos.forEach(function(elemento) {
                        // Si ya tiene el evento, no lo agregamos de nuevo
                        if (!elemento.classList.contains('evento-agregado')) {
                            elemento.addEventListener('click', function() {
                                if(VerificarAtributo('#"""+idtable+"""','disabled') == true){
                                    return;
                                }
                                
                                // Crear un objeto JSON directamente
                                var datosJson = {};
                                var iddato = "";
                                
                                // Eliminar la clase de selección previa
                                var elementosSeleccionados = document.querySelectorAll('.Seleccion');
                                elementosSeleccionados.forEach(function(el) {
                                    el.classList.remove('Seleccion');
                                });
                                
                                this.classList.add('Seleccion');

                                // Obtener las celdas de la fila seleccionada
                                var td = this.querySelectorAll('td');
                                td.forEach(function(tdElement) {
                                    var idcontrolsnow = tdElement.id;
                                    var numero = 0;

                                    // Verificar si es un campo que contiene '_id'
                                    if (idcontrolsnow.includes('_id')) {
                                        numero = 1;
                                    }

                                    iddato = tdElement.id.split('_');

                                    // Agregar la propiedad al objeto JSON con el contenido de la celda
                                    datosJson[iddato[numero]] = tdElement.textContent;
                                });

                                // Llamar al callback con el objeto JSON construido
                                callback(datosJson);
                            });

                            // Marcar el elemento como procesado para evitar duplicados
                            elemento.classList.add('evento-agregado');
                        }
                    });

                } catch (error) {
                    //console.log("Error en la función de la tabla: " + error);
                }
            }
            """+ScriptPaginacion+"""
            </script>""" 
        
       
    
    HtmlConteo = ""
    if MostralConteo == True:
        HtmlConteo = """
            <span class="badge bg-dark" style="font-size: 12px;width: max-content;">Cant: """+str(countFilas)+"""</span>
        """

    if reporte==True:
        ConteoHtml=""
        if conteo:
            ConteoHtml="""<span class="badge bg-dark" style="font-size: 12px;width: max-content;">Conteo: """+str(countFilas)+"""</span>"""
            
        HtmlReporte = """
            <div class="card-header bg-info text-center" style="font-size: 20px; color: #FFF; padding-top: 5px; padding-bottom: 5px;">
                <span class="fa fa-th-list"></span>
                <span>"""+Titulo+"""</span>
            </div>
            <div class="table-responsive">
            <table class="table table-hover table-striped" style="overflow: hidden">
            <thead>
                <tr>
                """+ColumnasTH.getvalue()+"""
                </tr>
            </thead>
            <tbody>
                """+FilasTD.getvalue()+"""
            </tbody>
            </table>
            """+ConteoHtml+"""
            </div>
        """
    
    Html = """
        """+Script+"""
        <div class="card" style="margin-bottom: 0px; margin-top:5px;">
        <div class="card-header bg-primary text-center" style="font-size: 20px; color: #FFF; padding-top: 5px; padding-bottom: 5px;">
            <span class="fa fa-th-list"></span>
            <span>"""+Titulo+"""</span>
        </div>
        <div class="table-responsive """+claseprincipal+"""">
        <table class="table table-hover table-striped" id='"""+idtable+"""'>
        <thead>
            <tr>
            """+ColumnasTH.getvalue()+"""
            </tr>
        </thead>
        <tbody>
            """+FilasTD.getvalue()+"""
        </tbody>
        </table>
        </div>
        """+HtmlConteo+"""
        </div>
    """
    if progressBar == True:
        socketio.emit(f"CerrarProgresoDeTablaReport_{sessionidusuario}", '')
    if TotalizarColumnas and not isinstance(TotalizarColumnas, bool) and any(TotalizarColumnas):
        if reporte==True:
            return Html,Totales,HtmlReporte
        else:
            return Html, Totales
    elif reporte==True:
        return Html,HtmlReporte
    return Html

def CrearFila(nombreClase, NumeralTabla, style, RespuestaValidacion):
    Fila = "<tr id='rows_"+NumeralTabla + "' class='"+nombreClase+" CursorPointer "+RespuestaValidacion+"' style='"+style+"'>"
    return Fila

def MarcarFilas(MarcarRows, SubColumnasDatos, DatosColumnas,row):
            while(True):
                campoValidar=MarcarRows[0]
                ValorValidar=MarcarRows[1]
                EntoncesValidacion=MarcarRows[2]
                ContrarioValidacion=MarcarRows[3]
                formato = type(ContrarioValidacion).__name__
                valor =SubDatosMarcar(SubColumnasDatos, DatosColumnas, campoValidar, row)
                if valor==ValorValidar:
                    return EntoncesValidacion
                else:
                    if formato == 'tuple':
                        MarcarRows=ContrarioValidacion
                    else:
                        return ContrarioValidacion

def CondicionParaTotalizar(ColumnaTotales, SubColumnasDatos, DatosColumnas,row):
    campoValidar=ColumnaTotales[0]
    ValorValidar=ColumnaTotales[1]
    valor =SubDatosMarcar(SubColumnasDatos, DatosColumnas, campoValidar, row)
    if valor==ValorValidar:
        return False
    else:
        return True

def ValidarLongitudDatos(*args):
    lengths = {len(arg) for arg in args if arg is not False}
    if len(lengths) > 1:
        raise ValueError("Las longitudes de los argumentos no coinciden")

def ProcesarSubDatos(SubColumnasDatos, countCol, col, row):
    columna = ""
    if SubColumnasDatos != False:
        tup = SubColumnasDatos[countCol]
        if tup != False:
            if len(tup) == 4:
                try:
                    columna = row[tup[0]][tup[1]][tup[2]]
                except Exception as ex:
                    try:
                        columna = tup[3]
                        if columna.count('<'):
                            columnanombre = tup[3].split('<')
                            columna = row[columnanombre[1]]
                        PCampo = row[tup[0]]
                        formato = type(PCampo).__name__

                        if formato == 'dict':
                            SCampo = PCampo[tup[1]]
                            formato2 = type(SCampo).__name__
                            if formato2 == 'dict':
                                columna = SCampo[tup[2]]
                            elif formato2 == 'list':
                                for Json in SCampo:
                                    columna = Json[tup[2]]

                        elif formato == 'list':
                            for Json in PCampo:
                                SCampo = Json[tup[1]]

                                formato2 = type(SCampo).__name__
                                if formato2 == 'dict':
                                    columna = SCampo[tup[2]]
                                elif formato2 == 'list':
                                    for Json in SCampo:
                                        columna = Json[tup[2]]

                    except Exception as ex:
                        columna = tup[2]
            else:
                try:
                    columna = row[tup[0]][tup[1]]
                except Exception as ex:
                    try:
                        columna = tup[2]
                        if columna.count('<'):
                            columnanombre = tup[2].split('<')
                            columna = row[columnanombre[1]]

                        for Json in row[tup[0]]:
                            columna = Json[tup[1]]
                    except Exception as ex:
                        columna = tup[2]
        else:
            columna = row[col]
    else:
        columna = row[col]
    
    return columna

def SubDatosMarcar(SubColumnasDatos, DatosColumnas,col,row):
    columna = ""
    countCol = 0
    for nombrecol in DatosColumnas:
        if col==nombrecol:
            break
        countCol+=1
    if SubColumnasDatos != False:
        tup = SubColumnasDatos[countCol]
        if tup != False:
            if len(tup) == 4:
                try:
                    columna = row[tup[0]][tup[1]][col]
                except Exception as ex:
                    try:
                        columna = tup[3]
                        if columna.count('<'):
                            columnanombre = tup[3].split('<')
                            columna = row[columnanombre[1]]
                        PCampo = row[tup[0]]
                        formato = type(PCampo).__name__

                        if formato == 'dict':
                            SCampo = PCampo[tup[1]]
                            formato2 = type(SCampo).__name__
                            if formato2 == 'dict':
                                columna = SCampo[col]
                            elif formato2 == 'list':
                                for Json in SCampo:
                                    columna = Json[col]

                        elif formato == 'list':
                            for Json in PCampo:
                                SCampo = Json[tup[1]]

                                formato2 = type(SCampo).__name__
                                if formato2 == 'dict':
                                    columna = SCampo[col]
                                elif formato2 == 'list':
                                    for Json in SCampo:
                                        columna = Json[col]

                    except Exception as ex:
                        columna = col
            else:
                try:
                    columna = row[tup[0]][col]
                except Exception as ex:
                    try:
                        columna = tup[2]
                        if columna.count('<'):
                            columnanombre = tup[2].split('<')
                            columna = row[columnanombre[1]]

                        for Json in row[tup[0]]:
                            columna = Json[col]
                    except Exception as ex:
                        columna = col
        else:
            columna = row[col]
    else:
        columna = row[col]
    
    return columna

def ProcesarSubFilas(SubFilas, row,FilasPlus: t.Union[list, bool] = False):
    #Subfilas=[("Documento","Tipo", "Valor"),("documento","tipo", "valor"),[('c'),('cxp','detalle',('cxp','p')),('nd'),('prod'),('nc','detalle')]]
    tupNomb = SubFilas[0]
    tupDtCol = SubFilas[1]
    DtLista = SubFilas[2]
    Html=""
    FilasTD = ""
    ColumnasTH = ""
    for col in tupNomb:
        ColumnasTH += '<th>'+col+'</th>'
        
    for Tupl in DtLista:
        try:
            tupDatos = Tupl
            tupFrt = SubFilas[3] if len(SubFilas) == 4 else False
            PCampo = row[tupDatos[0]]
            SCampo=None
            if len(tupDatos) == 3:
                if PCampo!=[] and PCampo !={}:
                    formato = type(PCampo).__name__
                    if formato == 'dict':
                        SCampo = PCampo[tupDatos[1]]

                    elif formato == 'list':
                        for Json in PCampo:
                            SCampo = Json[tupDatos[1]]
                            break
                
                    Datos=SCampo
                    DatosColumnas=tupDtCol
                    FormatoColumnas=tupFrt
                else:
                    TCampoTup = tupDatos[2]
                    PCampo = row[TCampoTup[0]]
                    if len(TCampoTup) == 2:
                        formato = type(PCampo).__name__
                        if formato == 'dict':
                            SCampo = PCampo[TCampoTup[1]]

                        elif formato == 'list':
                            for Json in PCampo:
                                SCampo = Json[TCampoTup[1]]
                                break

                        Datos=SCampo
                        DatosColumnas=tupDtCol
                        FormatoColumnas=tupFrt
                    elif len(TCampoTup) == 1:
                        Datos=PCampo
                        DatosColumnas=tupDtCol
                        FormatoColumnas=tupFrt
            elif len(tupDatos) == 2:
                formato = type(PCampo).__name__
                if formato == 'dict':
                    SCampo = PCampo[tupDatos[1]]

                elif formato == 'list':
                    for Json in PCampo:
                        SCampo = Json[tupDatos[1]]
                        break

                Datos=SCampo
                DatosColumnas=tupDtCol
                FormatoColumnas=tupFrt
            elif len(tupDatos) == 1:
                Datos=PCampo
                DatosColumnas=tupDtCol
                FormatoColumnas=tupFrt
            FilasTD+= HtmlSubfilas(Datos,DatosColumnas,FormatoColumnas,FilasPlus)
        except Exception as ex:
            FilasTD+=""
            pass
    Html = """
    <tr>
        <td colspan="12">
            <table class="table" style="width:99.5%;margin-left: 10px;">
                <tr style="background-color: #c9dadda1;">
                    """+ColumnasTH+"""
                </tr>
                """+FilasTD+"""
            </table>
        </td>
    </tr>
    """
    return Html
        
def HtmlSubfilas(Datos: t.Union[list, dict],
                 DatosColumnas: t.Union[tuple, tuple], FormatoColumnas: t.Union[tuple, bool] = False,FilasPlus: t.Union[list, bool] = False):
    
    countCol = 0
    ColumnasTD = ""
    FilasTD = ""
    formato = type(Datos).__name__
    if formato == 'dict':
        row = Datos
        style="background-color: #e9f1f5;" if FilasPlus != False else ""
        FilasTD += "<tr style='"+style+"'>"
        for col in DatosColumnas:
            columna = row[col]
            if FormatoColumnas != False:
                columna = Formatos(FormatoColumnas, countCol, columna)

            ColumnasTD += "<td class='text-wrap'>"+str(columna)+"</td>"
            countCol += 1

        if FilasPlus != False:
            FilasTD += ColumnasTD 
            # Dt, NombColumnas, DtColumnas, FrtColumnas=ProcesarSub(FilasPlus, row)
            # DtFilasPlus = HtmlfilasPlus(Datos=Dt, NombreColumnas=NombColumnas, DatosColumnas=DtColumnas, FormatoColumnas=FrtColumnas)
            DtFilasPlus = ProcesarFilasPlus(FilasPlus,row)
            
            FilasTD += DtFilasPlus+"</tr>"
        else:
            FilasTD += ColumnasTD+"</tr>"
        ColumnasTD = ""
        countCol = 0

    elif formato == 'list':
        for row in Datos:
            style="background-color: #e9f1f5;" if FilasPlus != False else ""
            FilasTD += "<tr style='"+style+"'>"
            for col in DatosColumnas:
                columna = row[col]
                if FormatoColumnas != False:
                    columna = Formatos(FormatoColumnas, countCol, columna)

                ColumnasTD += "<td class='text-wrap'>"+str(columna)+"</td>"
                countCol += 1
            if FilasPlus != False:
                FilasTD += ColumnasTD 
                # Dt, NombColumnas, DtColumnas, FrtColumnas=ProcesarSub(FilasPlus, row)
                # DtFilasPlus = HtmlfilasPlus(Datos=Dt, NombreColumnas=NombColumnas, DatosColumnas=DtColumnas, FormatoColumnas=FrtColumnas)
                DtFilasPlus = ProcesarFilasPlus(FilasPlus,row)
                FilasTD += DtFilasPlus+"</tr>"
            else:
                FilasTD += ColumnasTD+"</tr>"
                
            ColumnasTD = ""
            countCol = 0

    return FilasTD

def ProcesarFilasPlus(FilasPlus, row):
    #filasPlus=[("Cod.Pro", "Descripcion"),("idproducto", "descripcion"),[('p'),('c','detalle',('c','p')),('nd'),('prod'),('nc','detalle')]]
    tupNomb = FilasPlus[0]
    tupDtCol = FilasPlus[1]
    DtLista = FilasPlus[2]
    Html=""
    FilasTD = ""
    ColumnasTH = ""
    for col in tupNomb:
        ColumnasTH += '<th>'+col+'</th>'
        
    for Tupl in DtLista:
        try:
            tupDatos = Tupl
            tupFrt = FilasPlus[3] if len(FilasPlus) == 4 else False
            PCampo = row[tupDatos[0]]
            SCampo=None
            if len(tupDatos) == 3:
                if PCampo!=[] and PCampo !={}:
                    formato = type(PCampo).__name__
                    if formato == 'dict':
                        SCampo = PCampo[tupDatos[1]]

                    elif formato == 'list':
                        for Json in PCampo:
                            SCampo = Json[tupDatos[1]]
                            break
                
                    Datos=SCampo
                    DatosColumnas=tupDtCol
                    FormatoColumnas=tupFrt
                else:
                    TCampoTup = tupDatos[2]
                    PCampo = row[TCampoTup[0]]
                    if len(TCampoTup) == 2:
                        formato = type(PCampo).__name__
                        if formato == 'dict':
                            SCampo = PCampo[TCampoTup[1]]

                        elif formato == 'list':
                            for Json in PCampo:
                                SCampo = Json[TCampoTup[1]]
                                break

                        Datos=SCampo
                        DatosColumnas=tupDtCol
                        FormatoColumnas=tupFrt
                    elif len(TCampoTup) == 1:
                        Datos=PCampo
                        DatosColumnas=tupDtCol
                        FormatoColumnas=tupFrt
            elif len(tupDatos) == 2:
                formato = type(PCampo).__name__
                if formato == 'dict':
                    SCampo = PCampo[tupDatos[1]]

                elif formato == 'list':
                    for Json in PCampo:
                        SCampo = Json[tupDatos[1]]
                        break

                Datos=SCampo
                DatosColumnas=tupDtCol
                FormatoColumnas=tupFrt
            elif len(tupDatos) == 1:
                Datos=PCampo
                DatosColumnas=tupDtCol
                FormatoColumnas=tupFrt
            FilasTD+= HtmlfilasPlus(Datos,DatosColumnas,FormatoColumnas)
        except Exception as ex:
            FilasTD+=""
            pass
    
    Html = """
    <tr>
        <td colspan="12">
            <table class="table" style="width:99.5%;margin-left: 10px;">
                <tr style="background-color: #dde7e9;font-size: 13px;">
                    """+ColumnasTH+"""
                </tr>
                """+FilasTD+"""
            </table>
        </td>
    </tr>
    """
    return Html

def HtmlfilasPlus(Datos: t.Union[list, dict],
                 DatosColumnas: t.Union[tuple, tuple], FormatoColumnas: t.Union[tuple, bool] = False):
    
    countCol = 0
    ColumnasTD = ""
    FilasTD = ""
    formato = type(Datos).__name__

    if formato == 'dict':
        row = Datos
        FilasTD += "<tr>"
        for col in DatosColumnas:
            columna = row[col]
            if FormatoColumnas != False:
                columna = Formatos(FormatoColumnas, countCol, columna)

            ColumnasTD += "<td class='text-wrap'>"+str(columna)+"</td>"
            countCol += 1

        FilasTD += ColumnasTD+"</tr>"
        ColumnasTD = ""
        countCol = 0

    elif formato == 'list':
        for row in Datos:
            FilasTD += "<tr class='CursorPointer'>"
            for col in DatosColumnas:
                columna = row[col]
                if FormatoColumnas != False:
                    columna = Formatos(FormatoColumnas, countCol, columna)

                ColumnasTD += "<td class='text-wrap'>"+str(columna)+"</td>"
                countCol += 1

            FilasTD += ColumnasTD+"</tr>"
            ColumnasTD = ""
            countCol = 0

    return FilasTD

@lru_cache(maxsize=128)
def Formatos(FormatoColumnas, countCol, columna):
    formato = str(FormatoColumnas[countCol])
    if formato == "date":
        columna = Tools.DateFormat(columna)
    if formato == "datetime":
        columna = Tools.DateTimeFormat(columna)
    if formato == "moneda":
        columna = Tools.FormatoMoneda(columna)
    if formato == "encriptar":
        columna = Tools.Encriptar(columna)
    if formato.count("zfill"):
        long = formato.split('_')
        columna = str(columna).zfill(Tools.StrToInt(long[1]))
    return columna

def CrearTablaReport(Datos: t.Union[list, list],
                     NombreColumnas: t.Union[tuple, tuple] = None,
                     DatosColumnas: t.Union[tuple, tuple] = None,
                     ClassColumnas: t.Union[tuple, tuple] = None,
                     FormatoColumnas: t.Union[tuple, bool] = False,
                     TotalizarColumnas: t.Union[tuple, bool] = False,
                     ColumnasJson: t.Union[list, dict] = None,
                     CondicionTotalizar: t.Union[tuple, bool] = False,
                     SubColumnasDatos: t.Union[list, bool] = False,
                     SubFilas: t.Union[list, bool] = False,
                     FilasPlus: t.Union[list, bool] = False,
                     MarcarRows:t.Union[tuple, bool] = False,conteo=True,progressBar=False,sessionidusuario = None):

    # Si se proporciona ColumnasJson, convertir al formato anterior 
    if ColumnasJson:
        NombreColumnas = tuple(col[COLUMNA] for col in ColumnasJson)
        DatosColumnas = tuple(col[DATO] for col in ColumnasJson)
        ClassColumnas = tuple(col.get(CLASS, "") for col in ColumnasJson)
        FormatoColumnas = tuple(col.get(FORMATO, "") for col in ColumnasJson)
        TotalizarColumnas = tuple(col.get(TOTALIZAR, False) for col in ColumnasJson)
        SubColumnasDatos = tuple(col.get(SUBDATOS, False) for col in ColumnasJson)
        
    ValidarLongitudDatos(NombreColumnas, DatosColumnas, ClassColumnas, FormatoColumnas, TotalizarColumnas, SubColumnasDatos)
    try:
        if progressBar==True:
            tamano_datos = len(Datos)
    except Exception as e:
        pass

    countCol = 0
    ColumnasTH = StringIO()
    Totales = {}
    for col in NombreColumnas:
        ColumnasTH.write(f'<th scope="col" class="{ClassColumnas[countCol]}">{col}</th>')
        countCol += 1

    countCol = 0
    if TotalizarColumnas and not isinstance(TotalizarColumnas, bool) and any(TotalizarColumnas):
        for col in DatosColumnas:
            Totalizar = TotalizarColumnas[countCol]
            if Totalizar == True:
                Totales.update({
                    'T'+col: 0.00
                })
            countCol += 1

    countCol = 0
    countFilas = 0
    emitirEnD=0
    ColumnasTD = StringIO()
    FilasTD = StringIO()
    if Datos == [] or Datos is None:
        ColumnasTH = StringIO()
        FilasTD = StringIO()
        FilasTD.write("<div class='text-center'>NO SE ENCONTRARON DATOS.</div>")
    else:
        for row in Datos:
            NumeralTabla = str(countFilas)
            style="background-color: #97d2ea;" if SubFilas != False else ""
            
            if MarcarRows != False:
                Respuesta=MarcarFilas(MarcarRows,SubColumnasDatos,DatosColumnas,row)
                FilasTD.write(CrearFila('', NumeralTabla, style, Respuesta))
            else:
                FilasTD.write(f"<tr id='rows_{NumeralTabla}' class='' style='{style}'>")
            
            countFilas += 1
            for col in DatosColumnas:
                columna = ""
                if SubColumnasDatos != False:
                    tup = SubColumnasDatos[countCol]
                    if tup != False:
                        if len(tup) == 4:
                            try:
                                columna = row[tup[0]][tup[1]][tup[2]]
                            except Exception as ex:
                                try:
                                    columna = tup[3]
                                    if columna.count('<'):
                                        columnanombre = tup[3].split('<')
                                        columna = row[columnanombre[1]]
                                    PCampo = row[tup[0]]
                                    formato = type(PCampo).__name__

                                    if formato == 'dict':
                                        SCampo = PCampo[tup[1]]
                                        formato2 = type(SCampo).__name__
                                        if formato2 == 'dict':
                                            columna = SCampo[tup[2]]
                                        elif formato2 == 'list':
                                            for Json in SCampo:
                                                columna = Json[tup[2]]

                                    elif formato == 'list':
                                        for Json in PCampo:
                                            SCampo = Json[tup[1]]

                                            formato2 = type(SCampo).__name__
                                            if formato2 == 'dict':
                                                columna = SCampo[tup[2]]
                                            elif formato2 == 'list':
                                                for Json in SCampo:
                                                    columna = Json[tup[2]]

                                except Exception as ex:
                                    columna = tup[2]
                        else:
                            try:
                                columna = row[tup[0]][tup[1]]
                            except Exception as ex:
                                try:
                                    columna = tup[2]
                                    if columna.count('<'):
                                        columnanombre = tup[2].split('<')
                                        columna = row[columnanombre[1]]

                                    for Json in row[tup[0]]:
                                        columna = Json[tup[1]]
                                except Exception as ex:
                                    columna = tup[2]
                    else:
                        columna = row[col]
                else:
                    columna = row[col]

                if FormatoColumnas != False:
                    columna = Formatos(FormatoColumnas, countCol, columna)

                if TotalizarColumnas and not isinstance(TotalizarColumnas, bool) and any(TotalizarColumnas):
                    Sumar = TotalizarColumnas[countCol]
                    condicion = CondicionParaTotalizar(CondicionTotalizar,SubColumnasDatos,DatosColumnas,row) if CondicionTotalizar != False else True
                    if Sumar == True and condicion==True:
                        Totales['T'+str(col)] += Tools.StrToFloat(columna)

                ColumnasTD.write(f'<td id="{col}_{NumeralTabla}" class="{ClassColumnas[countCol]} text-wrap">{columna}</td>')
                countCol += 1

            if SubFilas != False:
                FilasTD.write(ColumnasTD.getvalue())
                DtSubFilas=ProcesarSubFilas(SubFilas=SubFilas, row=row,FilasPlus=FilasPlus)
                FilasTD.write(DtSubFilas)
                FilasTD.write("</tr>")
            else:
                FilasTD.write(ColumnasTD.getvalue())
                FilasTD.write("</tr>")
                 
            #FilasTD += ColumnasTD+"</tr>"
            ColumnasTD = StringIO()
            countCol = 0
            emitirEnD+=1
            if progressBar == True and emitirEnD>=350:
                socketio.emit(f"ProgresoDeTablaReport_{sessionidusuario}", {'transcurrido': countFilas, 'total': tamano_datos, 'barra': True}) 
                time.sleep(0.5)
                emitirEnD=0
    
    ConteoHtml=""
    if conteo:
        ConteoHtml="""<span class="badge bg-dark" style="font-size: 12px;width: max-content;">Conteo: """+str(countFilas)+"""</span>"""
        
    # Convertir ColumnasTH y FilasTD a StringIO si son strings
    if isinstance(ColumnasTH, str):
        temp = StringIO()
        temp.write(ColumnasTH)
        ColumnasTH = temp

    if isinstance(FilasTD, str):
        temp = StringIO()
        temp.write(FilasTD)
        FilasTD = temp
    Html = f"""
        <div class="card-header bg-info text-center" style="font-size: 20px; color: #FFF; padding-top: 5px; padding-bottom: 5px;">
            <span class="fa fa-th-list"></span>
            <span>Detalle</span>
        </div>
        <div class="table-responsive">
        <table class="table table-hover table-striped" style="overflow: hidden">
        <thead>
            <tr>
            {ColumnasTH.getvalue()}
            </tr>
        </thead>
        <tbody>
            {FilasTD.getvalue()}
        </tbody>
        </table>
        {ConteoHtml}
        </div>
    """
    if progressBar == True:
        socketio.emit(f"CerrarProgresoDeTablaReport_{sessionidusuario}", '')
    if TotalizarColumnas and not isinstance(TotalizarColumnas, bool) and any(TotalizarColumnas):
        return Html, Totales
    return Html

def TableVacia(NombreColumnas=('Id', 'Email', 'Usuario', 'Clave', 'Edad'), AgregarClass=False,
               ClassColumnas=('Id', 'Email', 'Usuario', 'Clave', 'Edad'), Titulo="Detalle", idtable="table"):
    countCol = 0
    ColumnasTH = StringIO()
    for col in NombreColumnas:
        if AgregarClass:
            countColClass = 0
            for clases in ClassColumnas:
                if countColClass == countCol:
                    ColumnasTH.write(f'<th class={clases}>{col}</th>')
                countColClass += 1
        else:
            ColumnasTH.write(f'<th>{col}</th>')
        countCol += 1

    Html = f"""
        <div class="card" style="margin-bottom: 0px; margin-top:5px;">
        <div class="card-header bg-info text-center" style="font-size: 20px; color: #FFF; padding-top: 5px; padding-bottom: 5px;">
            <span class="fa fa-th-list"></span>
            <span>{Titulo}</span>
        </div>
        <div class="table-responsive AlturaGrid">
        <table class="table table-bordered table-hover table-condensed table-striped" id='{idtable}'>
        <thead>
        </thead>
        <tbody class="text-center">
              <div class='text-center'>NO SE ENCONTRARON DATOS.</div>
        </tbody>
        </table>
        </div>
        </div>
    """
    return Html

def process_rows(Datos, DatosColumnas):
    for row in Datos:
        processed_row = {}
        for col in DatosColumnas:
            processed_row[col] = row[col]
        yield processed_row