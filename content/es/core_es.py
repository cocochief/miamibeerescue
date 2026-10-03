# -*- coding: utf-8 -*-
"""Copia en español de la portada /es/, precios, solicitud, el formulario y el
marco de página (encabezado, pie, barra móvil). Escrita directamente en español."""

CORE_ES = {
    # ------------------------------------------------------------ marco de página
    "chrome": {
        "call": "Llamar",
        "text": "Foto por texto",
        "quote": "Cotización gratis",
        "quick_label": "Respuesta rápida",
        "alarm_title": "Si las abejas están picando a alguien",
        "skip": "Ir directo al contenido",
        "topline": "Contestamos a cualquier hora y le respondemos dentro de 24 horas, garantizado",
        "menu": "Abrir el menú",
        "og_alt": "Logotipo de Miami Bee Rescue: una abeja bajo un arco dorado estilo art déco",
        "dock_label": "Contacto rápido",
        "dock_call": "Llamar",
        "dock_text": "Texto",
        "dock_quote": "Cotizar",
        "behind_h": "Lo que pasa por dentro",
        "putback_h": "Cómo queda todo al terminar",
        "cost_h": "De qué depende el precio de este trabajo",
        "cost_more": "Ver todos los precios",
        "faq_h": "Preguntas frecuentes",
        "related_h": "Otros servicios relacionados",
        "fits_h": "Servicios que más se piden aquí",
        "near_h": "Zonas cercanas",
        "glance_label": "Datos de",
        "zonas_h": "Dónde aparece este problema en Miami-Dade",
        "kinds": {"city": "Ciudad", "town": "Pueblo", "village": "Villa", "unincorporated": "Zona no incorporada",
                  "neighborhood": "Barrio de la Ciudad de Miami", "area": "Zona"},
        "home_crumb": "Inicio",
        "footer": {
            "about": ("Sacamos colonias de abejas vivas de casas, edificios, patios y fincas, y las llevamos a "
                      "apicultores. Tenemos licencia y seguro, y entregamos certificados de seguro (COI) a "
                      "asociaciones y negocios que los piden."),
            "area": ("Trabajamos solo en el condado de Miami-Dade, desde la playa hasta las fincas del Redland "
                     "y hasta la línea del condado. No tenemos local: vamos a su propiedad."),
            "h_removal": "Servicios",
            "h_places": "Zonas",
            "h_company": "Más información",
            "fine": "Nunca exterminamos colonias. Usted conoce el precio antes de empezar.",
            "en_link": "Sitio en inglés",
        },
    },

    # ------------------------------------------------------------ formulario
    "form": {
        "heading": "Díganos dónde están las abejas",
        "intro": ("Con tres datos basta para empezar: su nombre, un teléfono y la ciudad o el barrio. Lo demás "
                  "nos ahorra preguntas cuando le devolvamos la llamada."),
        "text_line": "Si prefiere, mándenos una foto por mensaje de texto",
        "hours_line": "El teléfono se contesta de día y de noche",
        "labels": {"name": "Su nombre", "phone": "Teléfono", "location": "Ciudad o barrio",
                   "email": "Correo electrónico", "spot": "Dónde las ve", "urgency": "Qué tan urgente es",
                   "notes": "Algo más que debamos saber"},
        "placeholders": {"name": "Nombre y apellido", "phone": "Para devolverle la llamada",
                         "location": "Por ejemplo: Hialeah, Westchester, Doral",
                         "email": "Para mandarle la cotización",
                         "notes": "Código del portón, piso, mascotas, alergias, desde cuándo están"},
        "optional": "(opcional)",
        "choose": "Elija la opción más parecida",
        "spot_options": ["Pared o estuco", "Techo, tejas o ático", "Alero o plafón", "Palma u otro árbol",
                         "Contador de agua o caja de válvulas", "Cobertizo, garaje o almacén",
                         "Enjambre colgando al aire libre", "Balcón o área común del edificio", "Todavía no sé"],
        # the value stays in English so the lead email and the [EMERGENCY] tag work the same way
        "urgency_options": [("Planning ahead", "Sin prisa, estoy planificando"),
                            ("This week", "Pronto, idealmente esta semana"),
                            ("Bees getting inside", "Están entrando a la casa"),
                            ("Emergency: stinging now", "Emergencia: están picando a alguien ahora")],
        "submit": "Enviar mi solicitud",
        "fine": ("Usamos estos datos solo para responderle sobre sus abejas; no los agregamos a ninguna lista. "
                 "Si alguien tiene una reacción a una picadura, llame primero al 911."),
    },

    # ------------------------------------------------------------ portada /es/
    "home": {
        "title": "Remoción de abejas en Miami-Dade, sin matarlas",
        "desc": ("Sacamos abejas de paredes, techos de tejas, palmas y contadores de agua en Miami-Dade. La "
                 "colonia sale viva hacia un apicultor y reparamos el lugar."),
        "kicker": "Abejas vivas, fuera de su propiedad",
        "h1": "Remoción de abejas en Miami-Dade",
        "lede": ("¿Un ir y venir de abejas por una grieta del estuco, debajo de una teja o dentro de la caja del "
                 "contador? Llame, mande una foto por texto o pida su cotización gratis."),
        "trust": [("clock", "Contestamos 24/7 y garantizamos respuesta en 24 horas"),
                  ("bee", "Las abejas van vivas a un apicultor"),
                  ("shield", "Con licencia y seguro; certificados de seguro a pedido"),
                  ("home", "Nuestros contratistas con licencia reparan lo que se abre")],
        "quick": ("Una colonia que ya construyó panal dentro de una pared o un techo no se va sola, y si se fumiga, "
                  "el panal y la miel se quedan adentro pudriéndose. Lo correcto es abrir lo justo, sacar las "
                  "abejas con todo su panal, entregarlas a un apicultor y cerrar la entrada. Cuando la colonia "
                  "está a nivel del suelo y cerca de la superficie, el trabajo suele costar entre $300 y $400."),
        "triage_h": "¿Qué está viendo ahora mismo?",
        "triage_sub": "Elija lo que más se parezca a su caso. Cada opción le lleva a la página que explica qué hacer.",
        "triage": [
            {"tone": "red", "href": "/es/servicios/emergencias/", "icon": "alert",
             "head": "Las abejas están picando a alguien",
             "text": "Entre con todos a la casa, cierre puertas y ventanas, y llámenos. Esas llamadas se atienden primero.",
             "go": "Qué hacer ya"},
            {"tone": "gold", "href": "/es/servicios/enjambres/", "icon": "bee",
             "head": "Hay una bola de abejas colgando de una rama",
             "text": "Sin panal a la vista, en una cerca, un buzón o el espejo del carro. Lo más probable es que sea un enjambre de paso.",
             "go": "Sobre enjambres"},
            {"tone": "ink", "href": "/es/servicios/abejas-en-paredes/", "icon": "home",
             "head": "Entran y salen por un mismo hueco de la casa",
             "text": "Una fila constante por una grieta, un respiradero o una teja indica que ya hay panal adentro.",
             "go": "Abejas en paredes"},
            {"tone": "sand", "href": "/es/solicitar/", "icon": "chat",
             "head": "No estoy seguro de lo que es",
             "text": "Tómele una foto desde lejos y mándenosla por texto. Con eso podemos orientarle.",
             "go": "Mandar una foto"},
        ],
        "steps_h": "Así trabajamos, de principio a fin",
        "steps": [
            ("Usted nos contacta", "Llame o escriba a cualquier hora. Ayuda mucho saber desde cuándo ve las abejas y tener una foto del hueco por donde entran."),
            ("Revisamos antes de abrir", "Con una cámara térmica ubicamos el panal detrás del estuco o de las tejas, así la abertura es pequeña y precisa."),
            ("La colonia sale con vida", "Sacamos las abejas, la cría y el panal, y los acomodamos en una caja. No rociamos veneno en el hueco."),
            ("Limpiamos y sellamos", "Raspamos la cera y la miel que quedan para que nada fermente ni atraiga otro enjambre, y cerramos la entrada."),
            ("Reparación, si la desea", "Nuestros contratistas, techadores y pintores con licencia reponen el estuco, las tejas y la pintura."),
        ],
        "price_kicker": "Precios claros",
        "price_h": "Lo que suele costar",
        "price": ("Si las abejas están a nivel del suelo y cerca de la superficie, el trabajo ronda los $300 a $400. "
                  "Cuando el panal está en lo alto de un techo, dentro de un cielo raso o repartido en varias "
                  "cavidades, hace falta más tiempo y más reparación, y el total puede sumar miles de dólares. "
                  "La cotización no cuesta nada y se la damos antes de abrir.\n\n"
                  "Las emergencias de noche o en fin de semana cuestan más que una visita entre semana. Si lo "
                  "necesita para sus archivos, le mandamos fotos del trabajo y una factura detallada."),
        "price_more": "Ver la página de precios",
        "fig_low": "trabajo típico a nivel del suelo",
        "fig_high_b": "Hasta miles",
        "fig_high": "trabajos altos, ocultos o con reparación",
        "svcs_h": "Servicios",
        "svcs_sub": "Cada página explica cómo se resuelve ese caso en las casas y edificios de aquí.",
        "places_h": "Zonas",
        "places_sub": ("Estas zonas tienen su propia página aquí. Cubrimos todo Miami-Dade; las demás zonas "
                       "aparecen en el sitio en inglés."),
        "faqs_h": "Antes de llamar",
        "faqs": [
            ("¿Las abejas se van solas si las dejo tranquilas?",
             "Un enjambre que descansa al aire libre normalmente sigue su camino en uno o dos días, cuando las "
             "exploradoras eligen un lugar. Pero si ya están construyendo panal dentro de una pared o un techo, "
             "se quedan y la colonia sigue creciendo hasta que alguien la saque."),
            ("¿Puedo echarles insecticida y ya?",
             "El insecticida mata las abejas que se ven, pero deja dentro el panal, la miel y la cría muerta. "
             "Todo eso fermenta, mancha, atrae cucarachas y hormigas, y el olor invita a otro enjambre. Sacando "
             "la colonia viva se va todo de una vez."),
            ("¿Ustedes matan las abejas?",
             "No. No ofrecemos exterminio. Las abejas, la cría y el panal salen juntos en una caja y terminan "
             "en el apiario de un apicultor."),
            ("¿Tengo que estar en la casa?",
             "Depende. Para un enjambre en el patio o una caja en el césped, a veces basta con el código del "
             "portón y una llamada. Si hay que abrir una pared o un techo, alguien tiene que darnos acceso y "
             "aprobar el plan."),
        ],
        "form_h": "Pida su cotización gratis",
    },

    # ------------------------------------------------------------ precios
    "precios": {
        "title": "Cuánto cuesta sacar un panal en Miami-Dade",
        "desc": ("Cuánto cuesta sacar abejas en Miami-Dade: unos $300 a $400 a nivel del suelo y más cuando hay "
                 "altura o reparación. Cotización gratis antes de empezar."),
        "kicker": "Precios",
        "h1": "Cuánto cuesta la remoción de abejas en Miami-Dade",
        "lede": ("Dos cifras cubren la mayoría de los casos. Lo demás depende de la altura, de cuánto panal "
                 "construyeron y de lo que haya que reconstruir después."),
        "quick": ("Si la colonia se alcanza desde el suelo y está cerca de la superficie, cuente con unos $300 a "
                  "$400. Cuando el trabajo es en un techo, un alero alto, un cielo raso o varias secciones de "
                  "pared, y además hay que reparar, el total puede subir a miles de dólares. La cotización es "
                  "gratis y se da antes de abrir nada."),
        "tiers_h": "Los rangos",
        "tiers": [
            ("$300–$400", "A nivel del suelo y poco profundo",
             "Un contador de agua, una parte baja de la pared, la esquina de un cobertizo o un enjambre en un "
             "arbusto. Una visita, una abertura pequeña y la entrada sellada al terminar."),
            ("Hasta miles", "Alto, profundo o repartido, con reparación",
             "Panal debajo de las tejas, encima del cielo raso, en un alero alto o en varias cavidades. Hacen "
             "falta escaleras grandes o trabajo de techo, más horas y reconstruir la superficie."),
            ("Gratis", "La cotización",
             "Las fotos por texto nos ayudan a entender el trabajo, y el precio firme llega cuando vemos el lugar."),
            ("Más de noche", "Noches y fines de semana",
             "Una emergencia fuera del horario de semana cuesta más que una visita normal. Si nadie corre "
             "peligro, esperar a un día de semana le cuesta menos."),
        ],
        "drivers_h": "Qué hace subir o bajar el precio",
        "drivers": [
            ("Altura y acceso", "Todo lo que pase de una escalera común requiere más equipo, más seguridad y a veces un elevador."),
            ("Tiempo que llevan ahí", "Una colonia de pocas semanas tiene poco panal; una que lleva toda la temporada puede llenar la cavidad entera."),
            ("Qué cubre el panal", "El drywall y el alero de vinilo se abren fácil. El estuco sobre bloque, las tejas y los cielos rasos terminados piden más cuidado al abrir y al reponer."),
            ("Reparaciones", "Nuestros contratistas, techadores y pintores con licencia pueden dejarlo todo terminado; eso suma al total pero evita contratar a otra compañía."),
            ("Trámites de acceso", "Portones con guardia, juntas de condominio, reservas de ascensor y certificados de seguro llevan tiempo de coordinación."),
        ],
        "band": ("¿Quiere una idea del precio antes de decidir?",
                 "Mande por texto una foto de cerca de la entrada y otra más amplia de la pared o el techo."),
        "body": [
            ("Por qué fumigar termina saliendo caro",
             "Fumigar una colonia dentro de la pared parece lo más económico, pero deja kilos de panal y miel en "
             "la cavidad. Con el calor de Miami esa miel fermenta, traspasa la pintura y el drywall, y atrae "
             "hormigas, cucarachas y polillas de la cera. Además, el olor del panal viejo hace que otro enjambre "
             "escoja el mismo hueco. Pagar una vez por sacarlo todo suele costar menos que pagar dos veces.\n\n"
             "Por eso no cotizamos remociones que dejen panal adentro: si abrimos, limpiamos."),
            ("Fotos y factura cuando las necesite",
             "Antes de empezar usted recibe la cotización para aceptarla o no. Si una asociación, un dueño, un "
             "comprador o usted mismo necesita un registro, pídanos fotos del trabajo y una factura detallada "
             "con la remoción, la limpieza y la reparación en líneas separadas."),
        ],
        "faqs": [
            ("¿Cobran por venir a ver?",
             "La cotización es gratis. Muchas veces unas fotos por texto bastan para orientarle, y el precio "
             "firme se da cuando vemos el lugar."),
            ("¿Por qué cuesta más de noche o en fin de semana?",
             "Salir fuera de horario tiene un costo mayor para el equipo, y eso se refleja en la tarifa. Si las "
             "abejas no ponen a nadie en peligro, una visita entre semana le cuesta menos."),
            ("¿El precio incluye cerrar el hueco?",
             "Sí. Sellar la entrada que usaban las abejas es parte de cada remoción, porque un hueco abierto "
             "invita a la próxima colonia. Reponer el acabado, como la textura del estuco, las tejas o la "
             "pintura, es parte de la reparación y suma según lo que haya que rehacer."),
            ("¿Y si las abejas vuelven después de pagar?",
             "Si regresan a un punto que nosotros sellamos, volvemos a atenderlo. Así funciona la garantía de "
             "nuestro trabajo."),
        ],
        "form_h": "Pida su cotización gratis",
    },

    # ------------------------------------------------------------ solicitar
    "solicitar": {
        "title": "Cotización gratis para sacar abejas en Miami-Dade",
        "desc": ("Pida su cotización gratis para sacar abejas en cualquier parte de Miami-Dade. Con su nombre, "
                 "teléfono y zona empezamos; contestamos a cualquier hora."),
        "kicker": "Solicitar servicio",
        "h1": "Pida que saquen las abejas de su propiedad en Miami-Dade",
        "lede": "Llene el formulario corto, llámenos o mande una foto por texto. Como le quede más cómodo.",
        "quick": ("El formulario le llega directamente a quien agenda las remociones. Le devolvemos la llamada "
                  "desde nuestro número dentro de 24 horas, y si hay alguien recibiendo picaduras, ese caso va "
                  "primero. Si puede, mande también una foto de la entrada por texto: le da a quien le llame algo "
                  "concreto para revisar."),
        "alarm": ("Meta a todos adentro, personas y mascotas, y cierre las puertas. Si alguien tiene hinchazón "
                  "en la cara o la garganta, le cuesta respirar o recibió muchas picaduras, llame al 911. "
                  "Después llámenos directamente en vez de usar el formulario."),
        "form_h": "Su solicitud",
        "ways_h": "Otras formas de comunicarse",
        "ways": [
            ("phone", "Llamar", "Lo mejor cuando están picando o entrando a la casa. Una persona contesta a cualquier hora."),
            ("chat", "Foto por texto", "Desde una distancia segura, acerque la imagen a la entrada y mándela con el nombre de su barrio. Una segunda foto de toda la pared o el techo ayuda."),
            ("form", "Correo electrónico", "Útil para planificar con calma, para administradores con varias direcciones o para enviar documentos."),
        ],
        "body": [
            ("Qué pasa después de enviarlo",
             "Leemos los datos, miramos las fotos que mande y le llamamos desde nuestro número principal. En "
             "esa llamada le ayudamos a ver si parece un enjambre de paso o una colonia establecida y qué "
             "rango de precio podría aplicar; el precio firme se da al ver el lugar. Luego acordamos una hora que le convenga a "
             "usted, a su administrador o a la caseta del portón."),
        ],
    },

    # ------------------------------------------------------------ llms.txt
    "llms": {
        "heading": "Sección /es/",
        "intro": "Páginas escritas directamente para lectores hispanohablantes que buscan remoción de abejas en Miami-Dade.",
    },
}
