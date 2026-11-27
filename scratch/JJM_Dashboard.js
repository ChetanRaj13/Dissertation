function initMap(mapId, stLayerColor, stLayerWidth, distLayerColor, dtLayerWidth, jkColor, Cat, SubCat, Param, StCode, statename, info) {

    stLayerColor = [78, 121, 190, 1];
    G_StCode = StCode;
    G_DtCode = "000";
    G_DtName = "";
    G_Extent = "";
    var DtCode = "000";
    var DtId = "";
    var StId = "";
    var StName = "";
    var DtId = "";
    var DtName = "";
    G_Cat = Cat;
    G_SubCat = SubCat;
    G_Param = Param;
    //G_StName = statename;
    var map, dialog;
    var app = {};
    var exportexcel;
    var token = "";
    var encN = 1;
    var stPointlayer;
    //Lang = 'hi';
    require([
        //"dojo/dom-construct", "esri/dijit/BasemapGallery", "esri/dijit/BasemapToggle",
        "esri/map", "esri/geometry/webMercatorUtils",
        "esri/layers/FeatureLayer",
        "esri/dijit/Legend", "esri/dijit/Search", "esri/renderers/ScaleDependentRenderer",
        "esri/symbols/Font", "esri/geometry/Point",
        "esri/SpatialReference", "esri/graphic", "esri/lang",
        "esri/dijit/PopupTemplate",
        "esri/renderers/UniqueValueRenderer", "esri/symbols/TextSymbol",

        "esri/geometry/Extent",
        "esri/InfoTemplate", "esri/symbols/SimpleMarkerSymbol",
        "esri/symbols/PictureMarkerSymbol", "esri/symbols/SimpleLineSymbol",
        "esri/symbols/SimpleFillSymbol", "esri/renderers/SimpleRenderer",
        "esri/Color"
    ], function (

        Map, webMercatorUtils, FeatureLayer, Legend,
        Search, ScaleDependentRenderer, Font, Point, SpatialReference,
        Graphic, esriLang, PopupTemplate,
        UniqueValueRenderer, TextSymbol,

        Extent,
        InfoTemplate, SimpleMarkerSymbol, PictureMarkerSymbol,
        SimpleLineSymbol, SimpleFillSymbol,
        SimpleRenderer, Color
    ) {

        var bounds = new Extent({
            //"xmin": 7189291.79,
            //"ymin": 563260.13,
            //"xmax": 11244335.73,
            //"ymax": 4780505.83,

            // "xmin": 6244068.996960785, "ymin": 306917.7443137255, "xmax": 12173020.304607844, "ymax": 4524163.444313725,

            "xmin": 6321360.930938901, "ymin": 757244.6703530876, "xmax": 11633146.55451015, "ymax": 4461418.745367905,

            //"xmin": 6426873.743878103, "ymin": -382565.0581633749, "xmax": 11889281.61892204, "ymax": 4590411.071276626,
            "spatialReference": { "wkid": 102100 }
        });
        var map = new Map(mapId, {
            extent: bounds,
            zoom: 5,
            slider: false,
            "maxScale": 500, //0
            "minScale": 56000000, // 100000000/56000000
            showLabels: true
        });

        var statesColor = stLayerColor;
        var statesLine = new SimpleLineSymbol("solid", statesColor, 0.7);
        var statesSymbol = new SimpleFillSymbol("solid", statesLine, null);
        var statesRenderer = new SimpleRenderer(statesSymbol);

        var stateBoundryColor = new Color('rgba(255, 255, 255, 0)');
        var statesColor = stLayerColor;
        var statesLine = new SimpleLineSymbol("solid", statesColor, parseFloat(stLayerWidth));
        var statesSymbol = new SimpleFillSymbol("solid", statesLine, null);
        var statesRendererBoundry = new SimpleRenderer(statesSymbol);

        var districtsColor = new Color(distLayerColor);
        var districtsLine = new SimpleLineSymbol("solid", districtsColor, dtLayerWidth);
        var districtsSymbol = new SimpleFillSymbol("solid", districtsLine, null);
        var districtsRenderer = new SimpleRenderer(districtsSymbol);

        var stateLayer;
        var stateBoundry;
        var stateHGJpointLayer;
        var districtLayer;

        var origin = window.location.origin;

        stateLayer = new FeatureLayer(serviceUrl + '/0' + serviceUrlToken, {
            mode: FeatureLayer.MODE_ONDEMAND,
            outFields: ["STNAME", "STCODE11"],
            displayField: "STNAME",
            showLabels: false
        });
        stateBoundry = new FeatureLayer(serviceUrl + '/0' + serviceUrlToken, {
            mode: FeatureLayer.MODE_ONDEMAND,
            outFields: ["STNAME", "STCODE11"],
            displayField: "STNAME",
            showLabels: false
        });
        stateHGJpointLayer = new FeatureLayer(serviceUrl + '/0' + serviceUrlToken, {
            mode: FeatureLayer.MODE_ONDEMAND,
            outFields: ["STNAME", "STCODE11"],
            displayField: "STNAME",
            showLabels: false
        });

        if (serviceUrl_district == 'https://mapservice.gov.in/gismapservice/rest/services/BharatMapService/District_Boundary/MapServer') {
            districtLayer = new FeatureLayer(serviceUrl_district + '/0' + serviceUrlToken_district, {
                mode: FeatureLayer.MODE_ONDEMAND,
                outFields: ["dtname", "dtcode11", "stname", "stcode11"],
                displayField: "dtname",
                showLabels: false
            });
        }
        else if (serviceUrl_district == 'https://mapservice.gov.in/gismapservice/rest/services/BharatMapService/Admin_Boundary_District/MapServer') {
            districtLayer = new FeatureLayer(serviceUrl_district + '/1' + serviceUrlToken_district, {
                mode: FeatureLayer.MODE_ONDEMAND,
                outFields: ["dtname", "dtcode11", "stname", "stcode11"],
                displayField: "dtname",
                showLabels: false
            });
        }
        else {
            districtLayer = new FeatureLayer(serviceUrl + '/1' + serviceUrlToken, {
                mode: FeatureLayer.MODE_ONDEMAND,
                outFields: ["dtname", "dtcode11", "stname", "stcode11"],
                displayField: "dtname",
                showLabels: false
            });
        }

        stPointlayer = new esri.layers.GraphicsLayer();

        var defaultSymbol = new SimpleFillSymbol().setStyle(SimpleFillSymbol.STYLE_NULL);
        defaultSymbol.outline.setStyle(SimpleLineSymbol.STYLE_NULL);

        var s = new Search({
            enableInfoWindow: false,
            sources: [],
            zoomScale: 0,
            map: map
        }, "");
        s.startup();

        var d = new Search({
            enableLabel: true,
            enableInfoWindow: false,
            sources: [],
            map: map,
            autoNavigate: true,
            //zoom: 10
            zoomScale: 288895
        }, "");
        d.startup();

        doSearchState = function (stcode) {
            var sources = s.sources;
            var selectedValueS = stcode;

            sources.push({
                featureLayer: stateLayer,
                placeholder: "State",
                enableLabel: false,
                searchFields: ["STCODE11"],
                displayField: "STNAME",
                exactMatch: false,
                name: "State",
                outFields: ["*"],
                color: "#00ff00",
                infoTemplate: new InfoTemplate("StateInfo")

            });
            s.set("sources", sources);

            /*--------------If multiple results are found, it will default and select the first. -----*/

            s.sources[0].highlightSymbol = highlightSymbol1; //set the symbol for the highlighted symbol
            if (selectedValueS == "28") {
                var valueS = "37";
                s.search(valueS);
            } else {
                s.search(selectedValueS);
            }
        }

        StateColor();
        function StateColor() {
            var renderer = new UniqueValueRenderer(defaultSymbol, "STCODE11");

            var statesColor = new Color('#4E79BE');
            var statesColor = new Color('#4E79BE');
            if (G_Param == 0) {
                statesColor = new Color('#4E79BE');
            }
            else {
                statesColor = new Color([51, 26, 0, 1]);
            }
            //var statesColor = stLayerColor;
            var statesLine = new SimpleLineSymbol("solid", statesColor, 0.7);
            var statesSymbol = new SimpleFillSymbol("solid", statesLine, null);
            var statesRenderer = new SimpleRenderer(statesSymbol);
            if (Cat == "3") {
                renderer.addValue("01", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 1])));
            }
            else {
                renderer.addValue("01", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            }
            renderer.addValue("02", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("03", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("04", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("05", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("06", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("07", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("08", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("09", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("10", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("11", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("12", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("13", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("14", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("15", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("16", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("17", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("18", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("19", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("20", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("21", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("22", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("23", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("24", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("25", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("26", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("27", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("29", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("30", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("31", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), 4.0), new Color([255, 255, 255, 0.5])));
            renderer.addValue("32", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("33", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("34", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("35", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("36", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("37", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            renderer.addValue("38", new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), dtLayerWidth), new Color([255, 255, 255, 0.5])));
            /*random color genrate*/
            stateLayer.redraw();
            stateLayer.setRenderer(renderer);
            stateBoundry.setRenderer(statesRenderer);

        }
        map.addLayers([stateLayer, districtLayer]);

        // Hide District Layer Bydefault
        districtLayer.hide();
        CatOnChange = function (Cat) {
            G_Cat = Cat;
            G_SubCat = "0";
            G_Param = "0";
            ChangeMap(Cat, '0', "0");
        }
        DispalyHeader = function (Cat, SubCat, Param) {
            var mainHeader;
            var menu;
            var mapheader;
            var info_Section;
            var info_Section_desc;
            var table_Header_desc;
            var graph_HeaderDesc;
            if (Lang == 'en') {
                mainHeader = MainHeader['Cat']['SubCat']['Param'];
                menu = Menu['Cat']['SubCat']['Param'];
                mapheader = Map_Header['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
                info_Section = Section_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
                info_Section_desc = Section_InfoDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
                table_Header_desc = Table_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
                graph_HeaderDesc = Graph_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
            }
            else {
                mainHeader = MainHeader_hi['Cat']['SubCat']['Param'];
                menu = Menu_hi['Cat']['SubCat']['Param'];
                mapheader = Map_Header_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
                info_Section = Section_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
                info_Section_desc = Section_InfoDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
                table_Header_desc = Table_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
                graph_HeaderDesc = Graph_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
            }

            /******************Main Header*************************/
            $("#lblHead1").html("");
            $("#lblHead2").html("");
            $("#lblHead1").html(mainHeader.desc_head1);
            $("#lblHead2").html(mainHeader.desc_head2);

            /******************Mobile SubMenu*************************/
            $("#lbl_Head_HH_Sch").html("");
            $("#lblhh_Name").html("");
            $("#lblSch_Awc_Name").html("");
            $("#lbl_Head_HH_Sch").html(menu.desc_head_M);
            $("#lblhh_Name").html(menu.desc_head_hh_M);
            $("#lblSch_Awc_Name").html(menu.desc_head_schAwc_M);

            /******************Menu*************************/
            $("#lblMenu_HH").html("");
            $("#lblMenu_Sch_Awc").html("");
            $("#lblMenu_asp_aejes").html("");
            $("#lblMenu_IoT").html("");
            $("#lblMenu_WQ").html("");
            $("#lblMenu_HH").html(menu.desc_head_hh);
            $("#lblMenu_Sch_Awc").html(menu.desc_head_sch_awc);
            $("#lblMenu_asp_aejes").html(menu.desc_head_asp_jeaes);
            $("#lblMenu_IoT").html(menu.desc_head_IoT);
            $("#lblMenu_WQ").html(menu.desc_head_qu);
            $("#lblcitizen_corner").html(menu.desc_head_citizen_corner);

            /******************Map Header*************************/
            $("#lblMap_head").html("");
            $("#lblMap_National_St").html("");
            $("#lblMap_head").html(mapheader[0].desc_head);
            $("#lblMap_National_St").html(mapheader[0].desc_StName);

            /******************Info Header*************************/
            $("#lblInfo_head_M").html("");
            $("#lblInfo_head").html("");
            $("#lblInfo_National_St_M").html("");
            $("#lblInfo_National_St").html("");
            $("#lblInfo_HHG").html("");
            $("#lblInfo_HHG_M").html("");
            $("#lblGraph_Month_head").html("");
            $("#lblGraph_Month_head_M").html("");
            $("#lblTable_headAsOn").html("");
            $("#lblTable_head_Mi").html("");
            $("#lblGraph_StateWise").html("");

            $("#lblInfo_head_M").html(info_Section[0].desc_head);
            $("#lblInfo_head").html(info_Section[0].desc_head);
            $("#lblInfo_National_St_M").html(mapheader[0].desc_StName);
            $("#lblInfo_National_St").html(mapheader[0].desc_StName);
            $("#lblInfo_HHG").html(info_Section[0].desc_head_HarGharJal);
            $("#lblInfo_HHG_M").html(info_Section[0].desc_head_HarGharJal);
            $("#lblGraph_Month_head").html(info_Section[0].desc_head_graph_my);
            $("#lblGraph_Month_head_M").html(info_Section[0].desc_head_graph_my);
            $("#lblTable_headAsOn").html(info_Section[0].desc_head_table);
            $("#lblTable_head_Mi").html(info_Section[0].desc_head_table_mis);
            $("#lblGraph_StateWise").html(info_Section[0].desc_head_graph);

            $("#lblHGJMsg").html("");
            $("#lblHGJMsg_M").html("");

            $("#lblHGJMsg").html(info_Section[0].desc_head_note);
            $("#lblHGJMsg_M").html(info_Section[0].desc_head_note);

            $("#lblHGJMsg2").html("");
            $("#lblHGJMsg_M2").html("");

            $("#lblHGJMsg2").html(info_Section[0].desc_head_note_desc);
            $("#lblHGJMsg_M2").html(info_Section[0].desc_head_note_desc_M);

            $("#lblTable_head_HGJ").html(info_Section[0].desc_head_HarGharJal_village);

            /******************Household Connection desc *************************/
            $("#lblInfo_hh").html("");
            $("#lblInfo_hc").html("");
            $("#lblInfo_hc_AsOn").html("");
            $("#lblInfo_hc_Mi").html("");
            $("#lblInfo_hh_Mi").html("");

            $("#lblInfo_hh_M").html("");
            $("#lblInfo_hc_M").html("");
            $("#lblInfo_hc_AsOn_M").html("");
            $("#lblInfo_hc_Mi_M").html("");
            $("#lblInfo_hh_Mi_M").html("");

            $("#lblInfo_hh").html(info_Section_desc[0].desc_hhs);
            $("#lblInfo_hc").html(info_Section_desc[0].desc_hc);
            $("#lblInfo_hc_AsOn").html(info_Section_desc[0].desc_hc_AsOn);
            $("#lblInfo_hh_Mi").html(info_Section_desc[0].desc_hh_Mi);
            $("#lblInfo_hc_Mi").html(info_Section_desc[0].desc_hc_Mi);

            $("#lblInfo_hh_M").html(info_Section_desc[0].desc_hhs_M);
            $("#lblInfo_hc_M").html(info_Section_desc[0].desc_hc_M);
            $("#lblInfo_hc_AsOn_M").html(info_Section_desc[0].desc_hc_AsOn_M);
            $("#lblInfo_hh_Mi_M").html(info_Section_desc[0].desc_hh_Mi_M);
            $("#lblInfo_hc_Mi_M").html(info_Section_desc[0].desc_hc_Mi_M);

            $("#lbltblState_HGJ").html(table_Header_desc[0].desc_Name);
            $("#lbltblVillage_100PerTap").html(info_Section_desc[0].desc_100perTapcon_reported);
            $("#lbltblVillage_Certified").html(info_Section_desc[0].desc_certified_village);
            $("#lbltblVillage_Certified_Per").html(info_Section_desc[0].desc_certified_village_per);


            $("#lbltblState_HGJ_M").html(table_Header_desc[0].desc_Name_M);
            $("#lbltblVillage_100PerTap_M").html(info_Section_desc[0].desc_100perTapcon_reported_M);
            $("#lbltblVillage_Certified_M").html(info_Section_desc[0].desc_certified_village_M);
            $("#lbltblVillage_Certified_Per_M").html(info_Section_desc[0].desc_certified_village_per_M);

            $("#lbltblState_financial").html("");
            $("#lbltblState_financial_M").html("");
            $("#lbltblState_financial").html(table_Header_desc[0].desc_Name);
            $("#lbltblState_financial_M").html(table_Header_desc[0].desc_Name);

            $("#lbltblRelease_financial").html("");
            $("#lbltblRelease_financial_M").html("");
            $("#lbltblRelease_financial").html(table_Header_desc[0].desc_amount_cr);
            $("#lbltblRelease_financial_M").html(table_Header_desc[0].desc_amount_cr);

            $("#lblbudjectsaction_head").html("");
            $("#lblbudjectsaction_head_M").html("");
            $("#lblbudjectsaction_head").html(info_Section[0].desc_head_financial_progress_funddrawn);
            $("#lblbudjectsaction_head_M").html(info_Section[0].desc_head_financial_progress_funddrawn);

            $("#lblFinProgress_head").html("");
            $("#lblFinProgress_head_M").html("");
            $("#lblFinProgress_head").html(info_Section[0].desc_head_financial_progress_state);
            $("#lblFinProgress_head_M").html(info_Section[0].desc_head_financial_progress_state);



            $("#lbl100Per_State").html("");
            $("#lbl100Per_State_M").html("");
            $("#lbl100Per_District").html("");
            $("#lbl100Per_District_M").html("");
            $("#lbl100Per_Block").html("");
            $("#lbl100Per_Block_M").html("");
            $("#lbl100Per_Panchayat").html("");
            $("#lbl100Per_Panchayat_M").html("");
            $("#lbl100Per_Village").html("");
            $("#lbl100Per_Village_M").html("");


            $("#lbl100Per_District_Rep").html("");
            $("#lbl100Per_District_Rep_M").html("");
            $("#lbl100Per_Block_Rep").html("");
            $("#lbl100Per_Block_Rep_M").html("");
            $("#lbl100Per_Panchayat_Rep").html("");
            $("#lbl100Per_Panchayat_Rep_M").html("");
            $("#lbl100Per_Village_Rep").html("");
            $("#lbl100Per_Village_Rep_M").html("");

            $("#lbl100Per_District_C").html("");
            $("#lbl100Per_District_C_M").html("");
            $("#lbl100Per_Block_C").html("");
            $("#lbl100Per_Block_C_M").html("");
            $("#lbl100Per_Panchayat_C").html("");
            $("#lbl100Per_Panchayat_C_M").html("");
            $("#lbl100Per_Village_C").html("");
            $("#lbl100Per_Village_C_M").html("");

            $("#lbl100Per_State").html(info_Section_desc[0].desc_hhg_s);
            $("#lbl100Per_State_M").html(info_Section_desc[0].desc_hhg_s);

            $("#lbl100Per_State_C").html(info_Section_desc[0].desc_hhg_C);
            $("#lbl100Per_State_C_M").html(info_Section_desc[0].desc_hhg_C);

            $("#lbl100Per_District").html(info_Section_desc[0].desc_hhg_d);
            $("#lbl100Per_District_M").html(info_Section_desc[0].desc_hhg_d);
            $("#lbl100Per_Block").html(info_Section_desc[0].desc_hhg_b);
            $("#lbl100Per_Block_M").html(info_Section_desc[0].desc_hhg_b);
            $("#lbl100Per_Panchayat").html(info_Section_desc[0].desc_hhg_p);
            $("#lbl100Per_Panchayat_M").html(info_Section_desc[0].desc_hhg_p);
            $("#lbl100Per_Village").html(info_Section_desc[0].desc_hhg_v);
            $("#lbl100Per_Village_M").html(info_Section_desc[0].desc_hhg_v);



            $("#lbl100Per_District_Rep").html(info_Section_desc[0].desc_reported);
            $("#lbl100Per_District_Rep_M").html(info_Section_desc[0].desc_reported);
            $("#lbl100Per_Block_Rep").html(info_Section_desc[0].desc_reported);
            $("#lbl100Per_Block_Rep_M").html(info_Section_desc[0].desc_reported);
            $("#lbl100Per_Panchayat_Rep").html(info_Section_desc[0].desc_reported);
            $("#lbl100Per_Panchayat_Rep_M").html(info_Section_desc[0].desc_reported);
            $("#lbl100Per_Village_Rep").html(info_Section_desc[0].desc_reported);
            $("#lbl100Per_Village_Rep_M").html(info_Section_desc[0].desc_reported);

            $("#lbl100Per_District_C").html(info_Section_desc[0].desc_certified);
            $("#lbl100Per_District_C_M").html(info_Section_desc[0].desc_certified);
            $("#lbl100Per_Block_C").html(info_Section_desc[0].desc_certified);
            $("#lbl100Per_Block_C_M").html(info_Section_desc[0].desc_certified);
            $("#lbl100Per_Panchayat_C").html(info_Section_desc[0].desc_certified);
            $("#lbl100Per_Panchayat_C_M").html(info_Section_desc[0].desc_certified);
            $("#lbl100Per_Village_C").html(info_Section_desc[0].desc_certified);
            $("#lbl100Per_Village_C_M").html(info_Section_desc[0].desc_certified);

            $("#aId_St").html("");
            $("#aId_Dt").html("");
            $("#aId_St").html(info_Section_desc[0].desc_st);
            $("#aId_Dt").html(info_Section_desc[0].desc_dt);

            /******************table header *************************/


            $("#lbltblState").html("");
            $("#lbltblHH").html("");
            $("#lbltblHC").html("");
            $("#lbltblHC_per").html("");

            $("#lbltblState_M").html("");
            $("#lbltblHH_M").html("");
            $("#lbltblHC_M").html("");
            $("#lbltblHC_Per_M").html("");

            $("#lbltblState").html(table_Header_desc[0].desc_Name);
            $("#lbltblHH").html(table_Header_desc[0].desc_hh);
            $("#lbltblHC").html(table_Header_desc[0].desc_hc);
            $("#lbltblHC_per").html(table_Header_desc[0].desc_hc_per);

            $("#lbltblState_M").html(table_Header_desc[0].desc_Name_M);
            $("#lbltblHH_M").html(table_Header_desc[0].desc_hh_M);
            $("#lbltblHC_M").html(table_Header_desc[0].desc_hc_M);
            $("#lbltblHC_Per_M").html(table_Header_desc[0].desc_hc_per_M);


            $("#lbltblMiState").html("");
            $("#lbltblMiHH").html("");
            $("#lbltblMiHC").html("");
            $("#lbltblMi_HC_Per").html("");

            $("#lbltblMiState_M").html("");
            $("#lbltblMiHH_M").html("");
            $("#lbltblMiHC_M").html("");
            $("#lbltblMiHC_Per_M").html("");

            $("#lbltblMiState").html(table_Header_desc[0].desc_Name);
            $("#lbltblMiHH").html(table_Header_desc[0].desc_hh_Mis);
            $("#lbltblMiHC").html(table_Header_desc[0].desc_hc_Mis);
            $("#lbltblMi_HC_Per").html(table_Header_desc[0].desc_hc_Mis_per);

            $("#lbltblMiState_M").html(table_Header_desc[0].desc_Name_Mi);
            $("#lbltblMiHH_M").html(table_Header_desc[0].desc_hh_Mis_M);
            $("#lbltblMiHC_M").html(table_Header_desc[0].desc_hc_Mis_M);
            $("#lbltblMiHC_Per_M").html(table_Header_desc[0].desc_hc_Mis_per_M);

            $("#lblrbn1").text(graph_HeaderDesc[0].desc_btn1);
            $("#lblrbn2").text(graph_HeaderDesc[0].desc_btn2);

            if (Lang == 'en') {
                jjmLogoChangeLive.setAttribute('src', 'content/images/JJMlogo.png');
            }
            else {
                jjmLogoChangeLive.setAttribute('src', 'content/images/JJMlogo_hi.png');
            }
        }
        ChangeMapGraphics_State = function (Arrdt, Cat, SubCat, Param, StCode) {
            stateLayer.on("mouse-over", function (evt) {
                var stName = "${STNAME}";
                var stCode = "${STCODE11}";
                var stcode11 = esriLang.substitute(evt.graphic.attributes, stCode);
                var stateName = esriLang.substitute(evt.graphic.attributes, stName);
                var Total;
                var Value;
                var Per;
                map.setMapCursor("pointer");
                for (i = 0; i < Arrdt.length; i++) {
                    var stcode = Arrdt[i].KeyValue;
                    if (stcode == stcode11) {
                        Total = Arrdt[i].Total;
                        Value = Arrdt[i].Value;
                        Per = Arrdt[i].Per;
                        if (Lang == 'hi') {
                            stateName = Arrdt[i].Name_hi;
                        }
                        else {
                            stateName = Arrdt[i].Name;
                        }
                        break;
                    }
                }
                var Hover_desc_S
                if (Lang == 'hi') {
                    Hover_desc_S = Hover_desc_hi['Cat' + G_Cat]['SubCat' + G_SubCat]['Param' + G_Param];
                }
                else {
                    Hover_desc_S = Hover_desc['Cat' + G_Cat]['SubCat' + G_SubCat]['Param' + G_Param];
                }

                table = '<div>' + Hover_desc_S[0].desc_total + ' : <font color="orange">' + numberWithCommas(parseInt(Total), 0, 0) + '</font><br>' + Hover_desc_S[0].desc_value + ': <font color="orange">' + numberWithCommas(parseInt(Value), 0, 0) + '</font> <font color="white">(<font color="orange">' + Per + '</font>%)</font></div>';
                var content2 = esriLang.substitute(evt.graphic.attributes, table);
                map.infoWindow.resize(245, 180);
                map.infoWindow.setContent('' + toTitleCase(stateName) + '<hr>' + '  ' + content2);
                map.infoWindow.show(event.screenPoint, map.getInfoWindowAnchor(event.screenPoint));
            });
            stateLayer.on("mouse-out", function (evt) {
                map.infoWindow.hide();
                map.setMapCursor("default");
            });

        }
        ChangeMapGraphics = function (Arrdt, Cat, SubCat, Param, StCode) {
            districtLayer.on("mouse-over", function (evt) {
                var stName = "${stname}";
                var dtName = "${dtname}";
                var dtCode = "${dtcode11}";
                var dtcode11 = esriLang.substitute(evt.graphic.attributes, dtCode);
                var stateName = esriLang.substitute(evt.graphic.attributes, stName);
                var districtName = esriLang.substitute(evt.graphic.attributes, dtName);
                if (Param == "0") {
                    map.setMapCursor("pointer");
                }
                else {
                    map.setMapCursor("default");
                }
                var Total;
                var Value;
                var Per;
                for (i = 0; i < Arrdt.length; i++) {
                    var dtcode = Arrdt[i].KeyValue;
                    if (dtcode == dtcode11) {
                        Total = Arrdt[i].Total;
                        Value = Arrdt[i].Value;
                        Per = Arrdt[i].Per;
                        if (Lang == 'hi') {
                            districtName = Arrdt[i].Name_hi;
                        }
                        else {
                            districtName = Arrdt[i].Name;
                        }
                        break;
                    }
                }
                for (i = 0; i < DtPoint.length; i++) {
                    var dtcode = DtPoint[i].KeyValue;
                    if (dtcode == dtcode11) {
                        if (Lang == 'hi') {
                            stateName = DtPoint[i].StName_hi;
                        }
                        else {
                            stateName = DtPoint[i].StName;
                        }
                        break;
                    }
                }
                if (typeof Total == "undefined") {
                    Total = "0";
                }
                if (typeof Value == "undefined") {
                    Value = "0";
                }
                if (typeof Per == "undefined") {
                    Per = "0";
                }
                var Hover_desc_D;
                if (Lang == 'hi') {
                    Hover_desc_D = Hover_desc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
                }
                else {
                    Hover_desc_D = Hover_desc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
                }
                var table = "";
                table = '<div>' + Hover_desc_D[0].desc_total + ' : <font color="orange">' + numberWithCommas(parseInt(Total), 0, 0) + '</font><br>' + Hover_desc_D[0].desc_value + ': <font color="orange">' + numberWithCommas(parseInt(Value), 0, 0) + '</font> <font color="white">(<font color="orange">' + Per + '</font>%)</font></div>';

                var content2 = esriLang.substitute(evt.graphic.attributes, table);

                map.infoWindow.setContent('' + districtName + '' + ' (' + toTitleCase(stateName) + ')<hr>' + '  ' + content2);
                map.infoWindow.show(event.screenPoint, map.getInfoWindowAnchor(event.screenPoint));

            });
            districtLayer.on("mouse-out", function (evt) {
                map.setMapCursor("default");
                map.infoWindow.hide();
                //jQuery("#info").empty();
                //jQuery("#info").css("display", "none");
            });
        }

        changeLanguage = function (lang) {
            Lang = lang;
            sessionStorage.setItem("Lang", lang);
            ChangeMap(Cat, G_SubCat, G_Param);
            if (Lang == 'en') {
                $("#lnkhi").css("display", "block");
                $("#lnken").css("display", "none");
            }
            else {
                $("#lnkhi").css("display", "none");
                $("#lnken").css("display", "block");
            }
        }

        changeParam = function (param) {
            if (param == 0) {
                $("#aId_St").attr('class', '');
                $("#aId_Dt").attr('class', '');
                $("#aId_St").attr('class', 'jjm-pale-blue jjm-text-blue jjm-padding-small');
                $("#aId_Dt").attr('class', 'jjm-text-gray jjm-light-gray jjm-padding-small');
            }
            else if (param == 1) {
                $("#aId_St").attr('class', '');
                $("#aId_Dt").attr('class', '');
                $("#aId_St").attr('class', 'jjm-text-gray jjm-light-gray jjm-padding-small');
                $("#aId_Dt").attr('class', 'jjm-pale-blue jjm-text-blue jjm-padding-small');
            }
            G_Param = param;
            var obj = {};
            obj.StCode11 = encodeTxt(G_StCode);
            obj.Cat = encodeTxt(G_Cat);
            obj.SubCat = encodeTxt(G_SubCat);
            obj.Param = encodeTxt(G_Param);
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/BindDistrictMap',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {
                    if (G_Param == 0) {
                        fillColorState(data.d, Cat, G_SubCat, G_Param, G_StCode);
                        ChangeMapGraphics_State(data.d, Cat, G_SubCat, G_Param, G_StCode);
                    }
                    else {
                        fillColorDistrict(data.d, Cat, G_SubCat, G_Param, G_StCode);
                        ChangeMapGraphics(data.d, Cat, G_SubCat, G_Param, G_StCode);
                    }
                }
            });
        }
        $("#checkbox1").change(function () {
            if (this.checked) {
                G_Cat = 0;
                G_SubCat = 0;
            }
            else {
                G_Cat = 0;
                G_SubCat = 1;
            }
            if (G_SubCat == 0) {
                if (Lang == 'hi') {
                    $("#lblchk_toggles").text(getCurrentDate_hi() + ' तक');
                }
                else {
                    $("#lblchk_toggles").text('As on ' + getCurrentDate());
                }
            }
            else {
                if (Lang == 'hi') {
                    $("#lblchk_toggles").text("15 अगस्‍त 2019 तक");
                }
                else {
                    $("#lblchk_toggles").text("As on 15 Aug 2019");
                }
            }
            var obj = {};
            obj.StCode11 = encodeTxt(G_StCode);
            obj.Cat = encodeTxt(G_Cat);
            obj.SubCat = encodeTxt(G_SubCat);
            obj.Param = encodeTxt(G_Param);
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/BindDistrictMap',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {
                    if (G_StCode == "0") {
                        $("#imgBtnHomeOuter").hide();
                    }
                    else {
                        doSearchState(G_StCode);
                        $("#imgBtnHomeOuter").show();

                    }
                    if (G_Param == 0) {
                        fillColorState(data.d, Cat, G_SubCat, G_Param, G_StCode);
                        ChangeMapGraphics_State(data.d, Cat, G_SubCat, G_Param, G_StCode);
                    }
                    else {
                        fillColorDistrict(data.d, Cat, G_SubCat, G_Param, G_StCode);
                        ChangeMapGraphics(data.d, Cat, G_SubCat, G_Param, G_StCode);
                    }
                }
            });
        });
        ChangeMap = function (Cat, SubCat, Param) {
            DispalyHeader(Cat, G_SubCat, G_Param);
            $("#a0").text(getCurrentDate());
            G_Cat = Cat;
            G_SubCat = SubCat;
            G_Param = Param;

            if (G_SubCat == 0) {
                if (Lang == 'hi') {
                    $("#lblchk_toggles").text(getCurrentDate_hi() + ' तक');
                }
                else {
                    $("#lblchk_toggles").text('As on ' + getCurrentDate());
                }
            }
            else {
                if (Lang == 'hi') {
                    $("#lblchk_toggles").text("15 अगस्‍त 2019 तक");
                }
                else {
                    $("#lblchk_toggles").text("As on 15 Aug 2019");
                }
            }
            $("#financial_details").hide();
            $("#financial_tab").hide();
            $("#financial_details_M").hide();
            $("#financial_tab_M").hide();

            $("#div_HGJ_export").hide();
            $("#div_tbl_HGJ").hide();
            $("#lblcollapse_expend_financial").text("[+]");
            $("#lblcollapse_expend_financial_M").text("[+]");
            $("#lblcollapse_expend_HGJ").text("[+]");

            ChangeMap_Param(Cat, SubCat, Param);
        }
        ChangeMap_Param = function (Cat, SubCat, Param) {
            $(".se-pre-con").fadeIn("slow");
            $("#imgLoading").fadeIn("slow");
            //fillColorState(markers_st, Cat, SubCat, Param, G_StCode);
            G_Cat = Cat;
            G_SubCat = SubCat;
            G_Param = Param;
            var obj = {};
            obj.StCode11 = encodeTxt(G_StCode);
            obj.Cat = encodeTxt(Cat);
            obj.SubCat = encodeTxt(SubCat);
            obj.Param = encodeTxt(Param);
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/BindDistrictMap',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {
                    if (G_StCode == "0") {
                        $("#imgBtnHomeOuter").hide();
                    }
                    else {
                        doSearchState(G_StCode);
                        $("#imgBtnHomeOuter").show();

                    }
                    if (G_Param == 0) {
                        fillColorState(data.d, Cat, SubCat, Param, G_StCode);
                        ChangeMapGraphics_State(data.d, Cat, SubCat, Param, G_StCode);
                    }
                    else {
                        fillColorDistrict(data.d, Cat, SubCat, Param, G_StCode);
                        ChangeMapGraphics(data.d, Cat, SubCat, Param, G_StCode);
                    }

                }
            });
            fillDashboard_data(Cat, SubCat, Param, G_StCode, 0);
            getBudgetSanction_data(Cat, SubCat, Param, G_StCode);
            getStatewise_Financial_info(Cat, SubCat, Param, G_StCode, '2023-2024');
        }
        getfillDashboard_data = function (value) {

            var graph_HeaderDesc;
            if (Lang == 'hi') {
                graph_HeaderDesc = Graph_HeaderDesc_hi['Cat0']['SubCat0']['Param0'];
            }
            else {
                graph_HeaderDesc = Graph_HeaderDesc['Cat0']['SubCat0']['Param0'];
            }
            $("#ag2").text('');
            $("#ag0").text('');
            $("#ag2").text(graph_HeaderDesc[0].desc_Yearly_head);
            $("#ag0").text(graph_HeaderDesc[0].desc_Cumulative_head);

            $("#ag2_M").text('');
            $("#ag0_M").text('');
            $("#ag2_M").text(graph_HeaderDesc[0].desc_Yearly_head);
            $("#ag0_M").text(graph_HeaderDesc[0].desc_Cumulative_head);
            if (value == 0) {
                $("#li0").attr('class', '');
                $("#li1").attr('class', '');
                $("#li2").attr('class', '');
                $("#li0").attr('class', 'jjm-bottombar jjm-border-blue');
                $("#li1").attr('class', 'jjm-bottombar jjm-border-gray');
                $("#li2").attr('class', 'jjm-bottombar jjm-border-gray');

                $("#ag0").attr('class', '');
                $("#ag1").attr('class', '');
                $("#ag2").attr('class', '');
                $("#ag0").attr('class', 'list-group-item jjm-text-blue jjm-CoverageButton jjm-small');
                $("#ag1").attr('class', 'list-group-item jjm-text-gray jjm-QualityButton jjm-small');
                $("#ag2").attr('class', 'list-group-item jjm-text-gray jjm-QualityButton jjm-small');

                $("#li0_M").attr('class', '');
                $("#li1_M").attr('class', '');
                $("#li2_M").attr('class', '');
                $("#li0_M").attr('class', 'jjm-bottombar jjm-border-blue');
                $("#li1_M").attr('class', 'jjm-bottombar jjm-border-gray');
                $("#li2_M").attr('class', 'jjm-bottombar jjm-border-gray');

                $("#ag0_M").attr('class', '');
                $("#ag1_M").attr('class', '');
                $("#ag2_M").attr('class', '');
                $("#ag0_M").attr('class', 'list-group-item jjm-text-blue jjm-CoverageButton jjm-small');
                $("#ag1_M").attr('class', 'list-group-item jjm-text-gray jjm-QualityButton jjm-small');
                $("#ag2_M").attr('class', 'list-group-item jjm-text-gray jjm-QualityButton jjm-small');
            }
            else if (value == 1) {
                $("#li0").attr('class', '');
                $("#li1").attr('class', '');
                $("#li2").attr('class', '');
                $("#li0").attr('class', 'jjm-bottombar jjm-border-gray');
                $("#li1").attr('class', 'jjm-bottombar jjm-border-blue');
                $("#li2").attr('class', 'jjm-bottombar jjm-border-gray');

                $("#ag0").attr('class', '');
                $("#ag1").attr('class', '');
                $("#ag2").attr('class', '');
                $("#ag0").attr('class', 'list-group-item jjm-text-gray jjm-QualityButton jjm-small');
                $("#ag1").attr('class', 'list-group-item jjm-text-blue jjm-CoverageButton jjm-small');
                $("#ag2").attr('class', 'list-group-item jjm-text-gray jjm-QualityButton jjm-small');

                $("#li0_M").attr('class', '');
                $("#li1_M").attr('class', '');
                $("#li2_M").attr('class', '');
                $("#li0_M").attr('class', 'jjm-bottombar jjm-border-gray');
                $("#li1_M").attr('class', 'jjm-bottombar jjm-border-blue');
                $("#li2_M").attr('class', 'jjm-bottombar jjm-border-gray');

                $("#ag0_M").attr('class', '');
                $("#ag1_M").attr('class', '');
                $("#ag2_M").attr('class', '');
                $("#ag0_M").attr('class', 'list-group-item jjm-text-gray jjm-QualityButton jjm-small');
                $("#ag1_M").attr('class', 'list-group-item jjm-text-blue jjm-CoverageButton jjm-small');
                $("#ag2_M").attr('class', 'list-group-item jjm-text-gray jjm-QualityButton jjm-small');
            }
            else if (value == 2) {
                $("#li0").attr('class', '');
                $("#li1").attr('class', '');
                $("#li2").attr('class', '');
                $("#li0").attr('class', 'jjm-bottombar jjm-border-gray');
                $("#li1").attr('class', 'jjm-bottombar jjm-border-gray');
                $("#li2").attr('class', 'jjm-bottombar jjm-border-blue');

                $("#ag0").attr('class', '');
                $("#ag1").attr('class', '');
                $("#ag2").attr('class', '');
                $("#ag0").attr('class', 'list-group-item jjm-text-gray jjm-QualityButton jjm-small');
                $("#ag1").attr('class', 'list-group-item jjm-text-gray jjm-QualityButton jjm-small');
                $("#ag2").attr('class', 'list-group-item jjm-text-blue jjm-CoverageButton jjm-small');

                $("#li0_M").attr('class', '');
                $("#li1_M").attr('class', '');
                $("#li2_M").attr('class', '');
                $("#li0_M").attr('class', 'jjm-bottombar jjm-border-gray');
                $("#li1_M").attr('class', 'jjm-bottombar jjm-border-gray');
                $("#li2_M").attr('class', 'jjm-bottombar jjm-border-blue');

                $("#ag0_M").attr('class', '');
                $("#ag1_M").attr('class', '');
                $("#ag2_M").attr('class', '');
                $("#ag0_M").attr('class', 'list-group-item jjm-text-gray jjm-QualityButton jjm-small');
                $("#ag1_M").attr('class', 'list-group-item jjm-text-gray jjm-QualityButton jjm-small');
                $("#ag2_M").attr('class', 'list-group-item jjm-text-blue jjm-CoverageButton jjm-small');
            }
            var obj = {};
            obj.StCode11 = encodeTxt(G_StCode);
            obj.Cat = encodeTxt(G_Cat);
            obj.SubCat = encodeTxt(G_SubCat);
            obj.Param = encodeTxt(G_Param);
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/Bind_graph_monthly',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {

                    console.log(data);


                    var Total_HC_01042021 = 0;
                    var Total_HC_01042022 = 0;
                    var Total_HC_01042023 = 0;
                    var Total_HC_01042024 = 0;                   
                    var Total_HC_01042025 = 0;
                     //*****************************************************  iamsubhash24@gmail.com start   *********************************
                    var Total_HC_01042026 = 0;
                    //*****************************************************  iamsubhash24@gmail.com end    *********************************
                    var Total_Month_2020_21 = 0;
                    var HouseholdAsondate_Total = 0;
                    var HouseholdTapConAsondate_Total = 0;





                    var cumulativedata = 0;
                    var Apr = 0; var May = 0; var Jun = 0; var Jul = 0;
                    var Aug = 0; var Sep = 0; var Oct = 0; var Nov = 0;
                    var Dec = 0; var Jan = 0; var Feb = 0; var Mar = 0;
                    var Apr_2021_22 = 0; var May_2021_22 = 0; var Jun_2021_22 = 0; var Jul_2021_22 = 0;
                    var Aug_2021_22 = 0; var Sep_2021_22 = 0; var Oct_2021_22 = 0; var Nov_2021_22 = 0;
                    var Dec_2021_22 = 0; var Jan_2021_22 = 0; var Feb_2021_22 = 0; var Mar_2021_22 = 0;
                    var Apr_Prev_Y = 0; var May_Prev_Y = 0; var Jun_Prev_Y = 0; var Jul_Prev_Y = 0;
                    var Aug_Prev_Y = 0; var Sep_Prev_Y = 0; var Oct_Prev_Y = 0; var Nov_Prev_Y = 0;
                    var Dec_Prev_Y = 0; var Jan_Prev_Y = 0; var Feb_Prev_Y = 0; var Mar_Prev_Y = 0;

                    var Apr_2022_23 = 0; var May_2022_23 = 0; var Jun_2022_23 = 0; var Jul_2022_23 = 0;
                    var Aug_2022_23 = 0; var Sep_2022_23 = 0; var Oct_2022_23 = 0; var Nov_2022_23 = 0;
                    var Dec_2022_23 = 0; var Jan_2022_23 = 0; var Feb_2022_23 = 0; var Mar_2022_23 = 0;

                    var Apr_2023_24 = 0; var May_2023_24 = 0; var Jun_2023_24 = 0; var Jul_2023_24 = 0;
                    var Aug_2023_24 = 0; var Sep_2023_24 = 0; var Oct_2023_24 = 0; var Nov_2023_24 = 0;
                    var Dec_2023_24 = 0; var Jan_2023_24 = 0; var Feb_2023_24 = 0; var Mar_2023_24 = 0;
                    var HCPWS_22_23 = 0;

                    var Apr_2024_25 = 0; var May_2024_25 = 0; var Jun_2024_25 = 0; var Jul_2024_25 = 0;
                    var Aug_2024_25 = 0; var Sep_2024_25 = 0; var Oct_2024_25 = 0; var Nov_2024_25 = 0;
                    var Dec_2024_25 = 0; var Jan_2024_25 = 0; var Feb_2024_25 = 0; var Mar_2024_25 = 0;

                   
                    var Apr_2025_26 = 0; var May_2025_26 = 0; var Jun_2025_26 = 0; var Jul_2025_26 = 0;
                    var Aug_2025_26 = 0; var Sep_2025_26 = 0; var Oct_2025_26 = 0; var Nov_2025_26 = 0;
                    var Dec_2025_26 = 0; var Jan_2025_26 = 0; var Feb_2025_26 = 0; var Mar_2025_26 = 0;
                     //*****************************************************  iamsubhash24@gmail.com start   *********************************
                    var Apr_2026_27 = 0; var May_2026_27 = 0; var Jun_2026_27 = 0; var Jul_2026_27 = 0;
                    var Aug_2026_27 = 0; var Sep_2026_27 = 0; var Oct_2026_27 = 0; var Nov_2026_27 = 0;
                    var Dec_2026_27 = 0; var Jan_2026_27 = 0; var Feb_2026_27 = 0; var Mar_2026_27 = 0;
                    //*****************************************************  iamsubhash24@gmail.com end    *********************************


                    dataArr = [];
                    monthArrCum = [];

                    dataArr_M = [];
                    monthArr = [];

                    yearArr = [];
                    dataArr_Y = [];
                    var year01042019_Total = 0;
                    var year2019_20_Total = 0;
                    var year2020_21_Total = 0;

                    var year2021_22_Total = 0;
                    var year2022_23_Total = 0;
                    var year2023_24_Total = 0;
                    var year2024_25_Total = 0;
                    var year2025_26_Total = 0;

                    //*****************************************************  iamsubhash24@gmail.com start   *********************************
                    var year2026_27_Total = 0;
                    //*****************************************************  iamsubhash24@gmail.com end    *********************************



                    for (var i = 0; i < data.d.length; i++) {

                        HouseholdAsondate_Total += parseFloat(data.d[i].Total);
                        HouseholdTapConAsondate_Total += parseFloat(data.d[i].Value);

                        cumulativedata += parseFloat(data.d[i].hcpws);
                        Total_HC_01042021 += parseFloat(data.d[i].HC_01042021);
                        Total_HC_01042022 += parseFloat(data.d[i].HC_01042022);
                        Total_HC_01042023 += parseFloat(data.d[i].HC_01042023);
                        Total_HC_01042024 += parseFloat(data.d[i].HC_01042024);                        
                        Total_HC_01042025 += parseFloat(data.d[i].HC_01042025);
                        //*****************************************************  iamsubhash24@gmail.com start   *********************************
                        Total_HC_01042026 += parseFloat(data.d[i].HC_01042026);
                        //*****************************************************  iamsubhash24@gmail.com end    *********************************

                        Apr += parseFloat(data.d[i].Apr);
                        May += parseFloat(data.d[i].May);
                        Jun += parseFloat(data.d[i].Jun);
                        Jul += parseFloat(data.d[i].Jul);
                        Aug += parseFloat(data.d[i].Aug);
                        Sep += parseFloat(data.d[i].Sep);
                        Oct += parseFloat(data.d[i].Oct);
                        Nov += parseFloat(data.d[i].Nov);
                        Dec += parseFloat(data.d[i].Dec);
                        Jan += parseFloat(data.d[i].Jan);
                        Feb += parseFloat(data.d[i].Feb);
                        Mar += parseFloat(data.d[i].Mar);
                        Apr_2021_22 += parseFloat(data.d[i].Apr_2021_22);
                        May_2021_22 += parseFloat(data.d[i].May_2021_22);
                        Jun_2021_22 += parseFloat(data.d[i].Jun_2021_22);
                        Jul_2021_22 += parseFloat(data.d[i].Jul_2021_22);
                        Aug_2021_22 += parseFloat(data.d[i].Aug_2021_22);
                        Sep_2021_22 += parseFloat(data.d[i].Sep_2021_22);
                        Oct_2021_22 += parseFloat(data.d[i].Oct_2021_22);
                        Nov_2021_22 += parseFloat(data.d[i].Nov_2021_22);
                        Dec_2021_22 += parseFloat(data.d[i].Dec_2021_22);
                        Jan_2021_22 += parseFloat(data.d[i].Jan_2021_22);
                        Feb_2021_22 += parseFloat(data.d[i].Feb_2021_22);
                        Mar_2021_22 += parseFloat(data.d[i].Mar_2021_22);

                        Total_Month_2020_21 += parseFloat(data.d[i].Total_Month_2020_21);

                        Apr_2022_23 += parseFloat(data.d[i].Apr_2022_23);
                        May_2022_23 += parseFloat(data.d[i].May_2022_23);
                        Jun_2022_23 += parseFloat(data.d[i].Jun_2022_23);
                        Jul_2022_23 += parseFloat(data.d[i].Jul_2022_23);
                        Aug_2022_23 += parseFloat(data.d[i].Aug_2022_23);
                        Sep_2022_23 += parseFloat(data.d[i].Sep_2022_23);
                        Oct_2022_23 += parseFloat(data.d[i].Oct_2022_23);
                        Nov_2022_23 += parseFloat(data.d[i].Nov_2022_23);
                        Dec_2022_23 += parseFloat(data.d[i].Dec_2022_23);
                        Jan_2022_23 += parseFloat(data.d[i].Jan_2022_23);
                        Feb_2022_23 += parseFloat(data.d[i].Feb_2022_23);
                        Mar_2022_23 += parseFloat(data.d[i].Mar_2022_23);

                        Apr_2023_24 += parseFloat(data.d[i].Apr_2023_24);
                        May_2023_24 += parseFloat(data.d[i].May_2023_24);
                        Jun_2023_24 += parseFloat(data.d[i].Jun_2023_24);
                        Jul_2023_24 += parseFloat(data.d[i].Jul_2023_24);
                        Aug_2023_24 += parseFloat(data.d[i].Aug_2023_24);
                        Sep_2023_24 += parseFloat(data.d[i].Sep_2023_24);
                        Oct_2023_24 += parseFloat(data.d[i].Oct_2023_24);
                        Nov_2023_24 += parseFloat(data.d[i].Nov_2023_24);
                        Dec_2023_24 += parseFloat(data.d[i].Dec_2023_24);
                        Jan_2023_24 += parseFloat(data.d[i].Jan_2023_24);
                        Feb_2023_24 += parseFloat(data.d[i].Feb_2023_24);
                        Mar_2023_24 += parseFloat(data.d[i].Mar_2023_24);


                        Apr_2024_25 += parseFloat(data.d[i].Apr_2024_25);
                        May_2024_25 += parseFloat(data.d[i].May_2024_25);
                        Jun_2024_25 += parseFloat(data.d[i].Jun_2024_25);
                        Jul_2024_25 += parseFloat(data.d[i].Jul_2024_25);
                        Aug_2024_25 += parseFloat(data.d[i].Aug_2024_25);
                        Sep_2024_25 += parseFloat(data.d[i].Sep_2024_25);
                        Oct_2024_25 += parseFloat(data.d[i].Oct_2024_25);
                        Nov_2024_25 += parseFloat(data.d[i].Nov_2024_25);
                        Dec_2024_25 += parseFloat(data.d[i].Dec_2024_25);
                        Jan_2024_25 += parseFloat(data.d[i].Jan_2024_25);
                        Feb_2024_25 += parseFloat(data.d[i].Feb_2024_25);
                        Mar_2024_25 += parseFloat(data.d[i].Mar_2024_25);

                       
                        Apr_2025_26 += parseFloat(data.d[i].Apr_2025_26);
                        May_2025_26 += parseFloat(data.d[i].May_2025_26);
                        Jun_2025_26 += parseFloat(data.d[i].Jun_2025_26);
                        Jul_2025_26 += parseFloat(data.d[i].Jul_2025_26);
                        Aug_2025_26 += parseFloat(data.d[i].Aug_2025_26);
                        Sep_2025_26 += parseFloat(data.d[i].Sep_2025_26);
                        Oct_2025_26 += parseFloat(data.d[i].Oct_2025_26);
                        Nov_2025_26 += parseFloat(data.d[i].Nov_2025_26);
                        Dec_2025_26 += parseFloat(data.d[i].Dec_2025_26);
                        Jan_2025_26 += parseFloat(data.d[i].Jan_2025_26);
                        Feb_2025_26 += parseFloat(data.d[i].Feb_2025_26);
                        Mar_2025_26 += parseFloat(data.d[i].Mar_2025_26);
                     


                        //*****************************************************  iamsubhash24@gmail.com start   *********************************
                        Apr_2026_27 += parseFloat(data.d[i].Apr_2026_27);
                        May_2026_27 += parseFloat(data.d[i].May_2026_27);
                        Jun_2026_27 += parseFloat(data.d[i].Jun_2026_27);
                        Jul_2026_27 += parseFloat(data.d[i].Jul_2026_27);
                        Aug_2026_27 += parseFloat(data.d[i].Aug_2026_27);
                        Sep_2026_27 += parseFloat(data.d[i].Sep_2026_27);
                        Oct_2026_27 += parseFloat(data.d[i].Oct_2026_27);
                        Nov_2026_27 += parseFloat(data.d[i].Nov_2026_27);
                        Dec_2026_27 += parseFloat(data.d[i].Dec_2026_27);
                        Jan_2026_27 += parseFloat(data.d[i].Jan_2026_27);
                        Feb_2026_27 += parseFloat(data.d[i].Feb_2026_27);
                        Mar_2026_27 += parseFloat(data.d[i].Mar_2026_27);
                        //*****************************************************  iamsubhash24@gmail.com end    *********************************



                        Apr_Prev_Y += parseFloat(data.d[i].Apr_Prev_Y);
                        May_Prev_Y += parseFloat(data.d[i].May_Prev_Y);
                        Jun_Prev_Y += parseFloat(data.d[i].Jun_Prev_Y);
                        Jul_Prev_Y += parseFloat(data.d[i].Jul_Prev_Y);
                        Aug_Prev_Y += parseFloat(data.d[i].Aug_Prev_Y);
                        Sep_Prev_Y += parseFloat(data.d[i].Sep_Prev_Y);
                        Oct_Prev_Y += parseFloat(data.d[i].Oct_Prev_Y);
                        Nov_Prev_Y += parseFloat(data.d[i].Nov_Prev_Y);
                        Dec_Prev_Y += parseFloat(data.d[i].Dec_Prev_Y);
                        Jan_Prev_Y += parseFloat(data.d[i].Jan_Prev_Y);
                        Feb_Prev_Y += parseFloat(data.d[i].Feb_Prev_Y);
                        Mar_Prev_Y += parseFloat(data.d[i].Mar_Prev_Y);

                        year01042019_Total += parseFloat(data.d[i].HCPWS_01042019);
                        year2019_20_Total += parseFloat(data.d[i].HCPWS_19_20);
                        year2020_21_Total += parseFloat(data.d[i].HCPWS_20_21);
                        year2021_22_Total += parseFloat(data.d[i].HCPWS_21_22);
                        year2022_23_Total += parseFloat(data.d[i].HCPWS_22_23);
                        year2023_24_Total += parseFloat(data.d[i].HCPWS_23_24);
                        
                        year2024_25_Total += parseFloat(data.d[i].HCPWS_24_25);
                        //*****************************************************  iamsubhash24@gmail.com start     *********************************
                        year2025_26_Total += parseFloat(data.d[i].HCPWS_25_26);
                        



                    }

                  //  year2025_26_Total = parseFloat(HouseholdTapConAsondate_Total) - parseFloat(Total_HC_01042025);
                  //  HouseholdTapConPer = parseFloat(HouseholdTapConAsondate_Total * 100 / HouseholdAsondate_Total).toFixed(2);

                    year2026_27_Total = parseFloat(HouseholdTapConAsondate_Total) - parseFloat(Total_HC_01042026);
                    HouseholdTapConPer = parseFloat(HouseholdTapConAsondate_Total * 100 / HouseholdAsondate_Total).toFixed(2);
                    //*****************************************************  iamsubhash24@gmail.com end  changes  *********************************
                    var today = new Date();
                    var dd = today.getDate();
                    var date = '';
                    if (dd < 10) {
                        date = '0' + dd;
                    }
                    else {
                        date = dd;
                    }
                    var MonthId = today.getMonth() + 1;
                    var yearId = today.getFullYear();
                    var yyyy = today.getFullYear();
                    var monthname;
                    if (Lang == 'hi') {
                        monthname = monthNames_hi;
                    }
                    else {
                        monthname = monthNames;
                    }
                    if (value == 0) {
                        monthArrCum.push('15 ' + monthname[7] + ' 2019');
                        monthArrCum.push(monthname[2] + ' 2020');
                        dataArr.push(year01042019_Total);
                        dataArr.push(cumulativedata);

                        if (MonthId >= 3 && yearId == 2021) {

                            monthArrCum.push(monthname[3] + ' 2020');
                            monthArrCum.push(monthname[4] + ' 2020');
                            monthArrCum.push(monthname[5] + ' 2020');
                            monthArrCum.push(monthname[6] + ' 2020');
                            monthArrCum.push(monthname[7] + ' 2020');
                            monthArrCum.push(monthname[8] + ' 2020');
                            monthArrCum.push(monthname[9] + ' 2020');
                            monthArrCum.push(monthname[10] + ' 2020');
                            monthArrCum.push(monthname[11] + ' 2020');
                            dataArr.push(cumulativedata + Apr);
                            dataArr.push(cumulativedata + Apr + May);
                            dataArr.push(cumulativedata + Apr + May + Jun);
                            dataArr.push(cumulativedata + Apr + May + Jun + Jul);
                            dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug);
                            dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep);
                            dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct);
                            dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov);
                            dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec);


                            if (MonthId <= 1 && yearId == 2021) {
                                monthArrCum.push(monthname[0] + ' 2021');
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan);
                            }
                            else if (MonthId <= 2 && yearId == 2021) {
                                monthArrCum.push(monthname[0] + ' 2021');
                                monthArrCum.push(monthname[1] + ' 2021');
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb);
                            }
                            else if (MonthId <= 3 && yearId == 2021) {
                                monthArrCum.push(monthname[0] + ' 2021');
                                monthArrCum.push(monthname[1] + ' 2021');
                                monthArrCum.push(monthname[2] + ' 2021');
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb + Mar);
                            }
                            else if (MonthId <= 4 && yearId == 2021) {
                                monthArrCum.push(monthname[0] + ' 2021');
                                monthArrCum.push(monthname[1] + ' 2021');
                                monthArrCum.push(monthname[2] + ' 2021');
                                monthArrCum.push(monthname[3] + ' 2021');
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb + Mar);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22);
                            }
                            else if (MonthId <= 5 && yearId == 2021) {
                                monthArrCum.push(monthname[0] + ' 2021');
                                monthArrCum.push(monthname[1] + ' 2021');
                                monthArrCum.push(monthname[2] + ' 2021');
                                monthArrCum.push(monthname[3] + ' 2021');
                                monthArrCum.push(monthname[4] + ' 2021');
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb + Mar);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22);
                            }
                            else if (MonthId <= 6 && yearId == 2021) {
                                monthArrCum.push(monthname[0] + ' 2021');
                                monthArrCum.push(monthname[1] + ' 2021');
                                monthArrCum.push(monthname[2] + ' 2021');
                                monthArrCum.push(monthname[3] + ' 2021');
                                monthArrCum.push(monthname[4] + ' 2021');
                                monthArrCum.push(monthname[5] + ' 2021');
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb + Mar);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22);
                            }
                            else if (MonthId <= 7 && yearId == 2021) {
                                monthArrCum.push(monthname[0] + ' 2021');
                                monthArrCum.push(monthname[1] + ' 2021');
                                monthArrCum.push(monthname[2] + ' 2021');
                                monthArrCum.push(monthname[3] + ' 2021');
                                monthArrCum.push(monthname[4] + ' 2021');
                                monthArrCum.push(monthname[5] + ' 2021');
                                monthArrCum.push(date + ' ' + monthname[6] + ' 2021');
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb + Mar);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22);
                            }
                            else if (MonthId <= 8 && yearId == 2021) {
                                monthArrCum.push(monthname[0] + ' 2021');
                                monthArrCum.push(monthname[1] + ' 2021');
                                monthArrCum.push(monthname[2] + ' 2021');
                                monthArrCum.push(monthname[3] + ' 2021');
                                monthArrCum.push(monthname[4] + ' 2021');
                                monthArrCum.push(monthname[5] + ' 2021');
                                monthArrCum.push(monthname[6] + ' 2021');
                                monthArrCum.push(date + ' ' + monthname[7] + ' 2021');
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb + Mar);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22);
                            }
                            else if (MonthId <= 9 && yearId == 2021) {
                                monthArrCum.push(monthname[0] + ' 2021');
                                monthArrCum.push(monthname[1] + ' 2021');
                                monthArrCum.push(monthname[2] + ' 2021');
                                monthArrCum.push(monthname[3] + ' 2021');
                                monthArrCum.push(monthname[4] + ' 2021');
                                monthArrCum.push(monthname[5] + ' 2021');
                                monthArrCum.push(monthname[6] + ' 2021');
                                monthArrCum.push(monthname[7] + ' 2021');
                                monthArrCum.push(date + ' ' + monthname[8] + ' 2021');
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb + Mar);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22 + Sep_2021_22);
                            }
                            else if (MonthId <= 10 && yearId == 2021) {
                                monthArrCum.push(monthname[0] + ' 2021');
                                monthArrCum.push(monthname[1] + ' 2021');
                                monthArrCum.push(monthname[2] + ' 2021');
                                monthArrCum.push(monthname[3] + ' 2021');
                                monthArrCum.push(monthname[4] + ' 2021');
                                monthArrCum.push(monthname[5] + ' 2021');
                                monthArrCum.push(monthname[6] + ' 2021');
                                monthArrCum.push(monthname[7] + ' 2021');
                                monthArrCum.push(monthname[8] + ' 2021');
                                monthArrCum.push(date + ' ' + monthname[9] + ' 2021');
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb + Mar);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22 + Sep_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22 + Sep_2021_22 + Oct_2021_22);
                            }
                            else if (MonthId <= 11 && yearId == 2021) {
                                monthArrCum.push(monthname[0] + ' 2021');
                                monthArrCum.push(monthname[1] + ' 2021');
                                monthArrCum.push(monthname[2] + ' 2021');
                                monthArrCum.push(monthname[3] + ' 2021');
                                monthArrCum.push(monthname[4] + ' 2021');
                                monthArrCum.push(monthname[5] + ' 2021');
                                monthArrCum.push(monthname[6] + ' 2021');
                                monthArrCum.push(monthname[7] + ' 2021');
                                monthArrCum.push(monthname[8] + ' 2021');
                                monthArrCum.push(monthname[9] + ' 2021');
                                monthArrCum.push(date + ' ' + monthname[10] + ' 2021');
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb + Mar);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22 + Sep_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22 + Sep_2021_22 + Oct_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22 + Sep_2021_22 + Oct_2021_22 + Nov_2021_22);
                            }
                            else if (MonthId >= 12 && yearId == 2021) {
                                monthArrCum.push(monthname[0] + ' 2021');
                                monthArrCum.push(monthname[1] + ' 2021');
                                monthArrCum.push(monthname[2] + ' 2021');
                                monthArrCum.push(monthname[3] + ' 2021');
                                monthArrCum.push(monthname[4] + ' 2021');
                                monthArrCum.push(monthname[5] + ' 2021');
                                monthArrCum.push(monthname[6] + ' 2021');
                                monthArrCum.push(monthname[7] + ' 2021');
                                monthArrCum.push(monthname[8] + ' 2021');
                                monthArrCum.push(monthname[9] + ' 2021');
                                monthArrCum.push(monthname[10] + ' 2021');
                                monthArrCum.push(date + ' ' + monthname[11] + ' 2021');
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb);
                                dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb + Mar);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22 + Sep_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22 + Sep_2021_22 + Oct_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22 + Sep_2021_22 + Oct_2021_22 + Nov_2021_22);
                                dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22 + Sep_2021_22 + Oct_2021_22 + Nov_2021_22 + Dec_2021_22);
                            }
                        } else {
                            /* Year 2020 */
                            monthArrCum.push(monthname[3] + ' 2020');
                            monthArrCum.push(monthname[4] + ' 2020');
                            monthArrCum.push(monthname[5] + ' 2020');
                            monthArrCum.push(monthname[6] + ' 2020');
                            monthArrCum.push(monthname[7] + ' 2020');
                            monthArrCum.push(monthname[8] + ' 2020');
                            monthArrCum.push(monthname[9] + ' 2020');
                            monthArrCum.push(monthname[10] + ' 2020');
                            monthArrCum.push(monthname[11] + ' 2020');
                            dataArr.push(cumulativedata + Apr);
                            dataArr.push(cumulativedata + Apr + May);
                            dataArr.push(cumulativedata + Apr + May + Jun);
                            dataArr.push(cumulativedata + Apr + May + Jun + Jul);
                            dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug);
                            dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep);
                            dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct);
                            dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov);
                            dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec);

                            /* year 2021 */
                            monthArrCum.push(monthname[0] + ' 2021');
                            monthArrCum.push(monthname[1] + ' 2021');
                            monthArrCum.push(monthname[2] + ' 2021');
                            monthArrCum.push(monthname[3] + ' 2021');
                            monthArrCum.push(monthname[4] + ' 2021');
                            monthArrCum.push(monthname[5] + ' 2021');
                            monthArrCum.push(monthname[6] + ' 2021');
                            monthArrCum.push(monthname[7] + ' 2021');
                            monthArrCum.push(monthname[8] + ' 2021');
                            monthArrCum.push(monthname[9] + ' 2021');
                            monthArrCum.push(monthname[10] + ' 2021');
                            monthArrCum.push(monthname[11] + ' 2021');
                            dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan);
                            dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb);
                            dataArr.push(cumulativedata + Apr + May + Jun + Jul + Aug + Sep + Oct + Nov + Dec + Jan + Feb + Mar);
                            dataArr.push(Total_HC_01042021 + Apr_2021_22);
                            dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22);
                            dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22);
                            dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22);
                            dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22);
                            dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22 + Sep_2021_22);
                            dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22 + Sep_2021_22 + Oct_2021_22);
                            dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22 + Sep_2021_22 + Oct_2021_22 + Nov_2021_22);
                            dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22 + Sep_2021_22 + Oct_2021_22 + Nov_2021_22 + Dec_2021_22);

                            /* year 2022 */
                            monthArrCum.push(monthname[0] + ' 2022');
                            monthArrCum.push(monthname[1] + ' 2022');
                            monthArrCum.push(monthname[2] + ' 2022');
                            dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22 + Sep_2021_22 + Oct_2021_22 + Nov_2021_22 + Dec_2021_22 + Jan_2021_22);
                            dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22 + Sep_2021_22 + Oct_2021_22 + Nov_2021_22 + Dec_2021_22 + Jan_2021_22 + Feb_2021_22);
                            dataArr.push(Total_HC_01042021 + Apr_2021_22 + May_2021_22 + Jun_2021_22 + Jul_2021_22 + Aug_2021_22 + Sep_2021_22 + Oct_2021_22 + Nov_2021_22 + Dec_2021_22 + Jan_2021_22 + Feb_2021_22 + Mar_2021_22);

                            monthArrCum.push(monthname[3] + ' 2022');
                            monthArrCum.push(monthname[4] + ' 2022');
                            monthArrCum.push(monthname[5] + ' 2022');
                            monthArrCum.push(monthname[6] + ' 2022');
                            monthArrCum.push(monthname[7] + ' 2022');
                            monthArrCum.push(monthname[8] + ' 2022');
                            monthArrCum.push(monthname[9] + ' 2022');
                            monthArrCum.push(monthname[10] + ' 2022');
                            monthArrCum.push(monthname[11] + ' 2022');
                            monthArrCum.push(monthname[0] + ' 2023');
                            monthArrCum.push(monthname[1] + ' 2023');
                            monthArrCum.push(monthname[2] + ' 2023');
                            dataArr.push(Total_HC_01042022 + Apr_2022_23);
                            dataArr.push(Total_HC_01042022 + Apr_2022_23 + May_2022_23);
                            dataArr.push(Total_HC_01042022 + Apr_2022_23 + May_2022_23 + Jun_2022_23);
                            dataArr.push(Total_HC_01042022 + Apr_2022_23 + May_2022_23 + Jun_2022_23 + Jul_2022_23);
                            dataArr.push(Total_HC_01042022 + Apr_2022_23 + May_2022_23 + Jun_2022_23 + Jul_2022_23 + Aug_2022_23);
                            dataArr.push(Total_HC_01042022 + Apr_2022_23 + May_2022_23 + Jun_2022_23 + Jul_2022_23 + Aug_2022_23 + Sep_2022_23);
                            dataArr.push(Total_HC_01042022 + Apr_2022_23 + May_2022_23 + Jun_2022_23 + Jul_2022_23 + Aug_2022_23 + Sep_2022_23 + Oct_2022_23);
                            dataArr.push(Total_HC_01042022 + Apr_2022_23 + May_2022_23 + Jun_2022_23 + Jul_2022_23 + Aug_2022_23 + Sep_2022_23 + Oct_2022_23 + Nov_2022_23);
                            dataArr.push(Total_HC_01042022 + Apr_2022_23 + May_2022_23 + Jun_2022_23 + Jul_2022_23 + Aug_2022_23 + Sep_2022_23 + Oct_2022_23 + Nov_2022_23 + Dec_2022_23);
                            dataArr.push(Total_HC_01042022 + Apr_2022_23 + May_2022_23 + Jun_2022_23 + Jul_2022_23 + Aug_2022_23 + Sep_2022_23 + Oct_2022_23 + Nov_2022_23 + Dec_2022_23 + Jan_2022_23);
                            dataArr.push(Total_HC_01042022 + Apr_2022_23 + May_2022_23 + Jun_2022_23 + Jul_2022_23 + Aug_2022_23 + Sep_2022_23 + Oct_2022_23 + Nov_2022_23 + Dec_2022_23 + Jan_2022_23 + Feb_2022_23);
                            dataArr.push(Total_HC_01042022 + Apr_2022_23 + May_2022_23 + Jun_2022_23 + Jul_2022_23 + Aug_2022_23 + Sep_2022_23 + Oct_2022_23 + Nov_2022_23 + Dec_2022_23 + Jan_2022_23 + Feb_2022_23 + Mar_2022_23);


                            //----------------2023-2024----DATA BIND
                            monthArrCum.push(monthname[3] + ' 2023');
                            monthArrCum.push(monthname[4] + ' 2023');
                            monthArrCum.push(monthname[5] + ' 2023');
                            monthArrCum.push(monthname[6] + ' 2023');
                            monthArrCum.push(monthname[7] + ' 2023');
                            monthArrCum.push(monthname[8] + ' 2023');
                            monthArrCum.push(monthname[9] + ' 2023');
                            monthArrCum.push(monthname[10] + ' 2023');
                            monthArrCum.push(monthname[11] + ' 2023');
                            monthArrCum.push(monthname[0] + ' 2024');
                            monthArrCum.push(monthname[1] + ' 2024');
                            monthArrCum.push(monthname[2] + ' 2024');
                            dataArr.push(Total_HC_01042023 + Apr_2023_24);
                            dataArr.push(Total_HC_01042023 + Apr_2023_24 + May_2023_24);
                            dataArr.push(Total_HC_01042023 + Apr_2023_24 + May_2023_24 + Jun_2023_24);
                            dataArr.push(Total_HC_01042023 + Apr_2023_24 + May_2023_24 + Jun_2023_24 + Jul_2023_24);
                            dataArr.push(Total_HC_01042023 + Apr_2023_24 + May_2023_24 + Jun_2023_24 + Jul_2023_24 + Aug_2023_24);
                            dataArr.push(Total_HC_01042023 + Apr_2023_24 + May_2023_24 + Jun_2023_24 + Jul_2023_24 + Aug_2023_24 + Sep_2023_24);
                            dataArr.push(Total_HC_01042023 + Apr_2023_24 + May_2023_24 + Jun_2023_24 + Jul_2023_24 + Aug_2023_24 + Sep_2023_24 + Oct_2023_24);
                            dataArr.push(Total_HC_01042023 + Apr_2023_24 + May_2023_24 + Jun_2023_24 + Jul_2023_24 + Aug_2023_24 + Sep_2023_24 + Oct_2023_24 + Nov_2023_24);
                            dataArr.push(Total_HC_01042023 + Apr_2023_24 + May_2023_24 + Jun_2023_24 + Jul_2023_24 + Aug_2023_24 + Sep_2023_24 + Oct_2023_24 + Nov_2023_24 + Dec_2023_24);
                            dataArr.push(Total_HC_01042023 + Apr_2023_24 + May_2023_24 + Jun_2023_24 + Jul_2023_24 + Aug_2023_24 + Sep_2023_24 + Oct_2023_24 + Nov_2023_24 + Dec_2023_24 + Jan_2023_24);
                            dataArr.push(Total_HC_01042023 + Apr_2023_24 + May_2023_24 + Jun_2023_24 + Jul_2023_24 + Aug_2023_24 + Sep_2023_24 + Oct_2023_24 + Nov_2023_24 + Dec_2023_24 + Jan_2023_24 + Feb_2023_24);
                            dataArr.push(Total_HC_01042023 + Apr_2023_24 + May_2023_24 + Jun_2023_24 + Jul_2023_24 + Aug_2023_24 + Sep_2023_24 + Oct_2023_24 + Nov_2023_24 + Dec_2023_24 + Jan_2023_24 + Feb_2023_24 + Mar_2023_24);

                            ////*****************************************************  iamsubhash24@gmail.com start   *********************************












                            ////----------------2024-2025----DATA BIND
                            //monthArrCum.push(monthname[3] + ' 2024');
                            //monthArrCum.push(monthname[4] + ' 2024');
                            //monthArrCum.push(monthname[5] + ' 2024');
                            //monthArrCum.push(monthname[6] + ' 2024');
                            //monthArrCum.push(monthname[7] + ' 2024');
                            //monthArrCum.push(monthname[8] + ' 2024');
                            //monthArrCum.push(monthname[9] + ' 2024');
                            //monthArrCum.push(monthname[10] + ' 2024');
                            //monthArrCum.push(monthname[11] + ' 2024');
                            //monthArrCum.push(monthname[0] + ' 2025');
                            //monthArrCum.push(monthname[1] + ' 2025');
                            //monthArrCum.push(monthname[2] + ' 2025');
                            //dataArr.push(Total_HC_01042024 + Apr_2024_25);
                            //dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25);
                            //dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25 + Jun_2024_25);
                            //dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25 + Jun_2024_25 + Jul_2024_25);
                            //dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25 + Jun_2024_25 + Jul_2024_25 + Aug_2024_25);
                            //dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25 + Jun_2024_25 + Jul_2024_25 + Aug_2024_25 + Sep_2024_25);
                            //dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25 + Jun_2024_25 + Jul_2024_25 + Aug_2024_25 + Sep_2024_25 + Oct_2024_25);
                            //dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25 + Jun_2024_25 + Jul_2024_25 + Aug_2024_25 + Sep_2024_25 + Oct_2024_25 + Nov_2024_25);
                            //dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25 + Jun_2024_25 + Jul_2024_25 + Aug_2024_25 + Sep_2024_25 + Oct_2024_25 + Nov_2024_25 + Dec_2024_25);
                            //dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25 + Jun_2024_25 + Jul_2024_25 + Aug_2024_25 + Sep_2024_25 + Oct_2024_25 + Nov_2024_25 + Dec_2024_25 + Jan_2024_25);
                            //dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25 + Jun_2024_25 + Jul_2024_25 + Aug_2024_25 + Sep_2024_25 + Oct_2024_25 + Nov_2024_25 + Dec_2024_25 + Jan_2024_25 + Feb_2024_25);
                            //dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25 + Jun_2024_25 + Jul_2024_25 + Aug_2024_25 + Sep_2024_25 + Oct_2024_25 + Nov_2024_25 + Dec_2024_25 + Jan_2024_25 + Feb_2024_25 + Mar_2024_25);
                            ////----------------2025-2026----DATA BIND
                            //if (MonthId == 4 && yearId == 2025) {
                            //    monthArrCum.push('' + date + ' ' + monthname[3] + ' 2025');
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26);
                            //}
                            //else if (MonthId == 5 && yearId == 2025) {
                            //    monthArrCum.push(monthname[3] + ' 2025');
                            //    monthArrCum.push('' + date + ' ' + monthname[4] + ' 2025');
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26);
                            //}
                            //else if (MonthId == 6 && yearId == 2025) {
                            //    monthArrCum.push(monthname[3] + ' 2025');
                            //    monthArrCum.push(monthname[4] + ' 2025');
                            //    monthArrCum.push('' + date + ' ' + monthname[5] + ' 2025');
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26);
                            //}
                            //else if (MonthId == 7 && yearId == 2025) {
                            //    monthArrCum.push(monthname[3] + ' 2025');
                            //    monthArrCum.push(monthname[4] + ' 2025');
                            //    monthArrCum.push(monthname[5] + ' 2025');
                            //    monthArrCum.push('' + date + ' ' + monthname[6] + ' 2025');
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26);
                            //}
                            //else if (MonthId == 8 && yearId == 2025) {
                            //    monthArrCum.push(monthname[3] + ' 2025');
                            //    monthArrCum.push(monthname[4] + ' 2025');
                            //    monthArrCum.push(monthname[5] + ' 2025');
                            //    monthArrCum.push(monthname[6] + ' 2025');
                            //    monthArrCum.push('' + date + ' ' + monthname[7] + ' 2025');
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26);
                            //}
                            //else if (MonthId == 9 && yearId == 2025) {
                            //    monthArrCum.push(monthname[3] + ' 2025');
                            //    monthArrCum.push(monthname[4] + ' 2025');
                            //    monthArrCum.push(monthname[5] + ' 2025');
                            //    monthArrCum.push(monthname[6] + ' 2025');
                            //    monthArrCum.push(monthname[7] + ' 2025');
                            //    monthArrCum.push('' + date + ' ' + monthname[8] + ' 2025');
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26);
                            //}
                            //else if (MonthId == 10 && yearId == 2025)  {
                            //    monthArrCum.push(monthname[3] + ' 2025');
                            //    monthArrCum.push(monthname[4] + ' 2025');
                            //    monthArrCum.push(monthname[5] + ' 2025');
                            //    monthArrCum.push(monthname[6] + ' 2025');
                            //    monthArrCum.push(monthname[7] + ' 2025');
                            //    monthArrCum.push(monthname[8] + ' 2025');
                            //    monthArrCum.push('' + date + ' ' + monthname[9] + ' 2025');
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26);
                            //}
                           
                            //else if (MonthId == 11 && yearId == 2025) {
                            //    monthArrCum.push(monthname[3] + ' 2025');
                            //    monthArrCum.push(monthname[4] + ' 2025');
                            //    monthArrCum.push(monthname[5] + ' 2025');
                            //    monthArrCum.push(monthname[6] + ' 2025');
                            //    monthArrCum.push(monthname[7] + ' 2025');
                            //    monthArrCum.push(monthname[8] + ' 2025');
                            //    monthArrCum.push(monthname[9] + ' 2025');
                            //    monthArrCum.push('' + date + ' ' + monthname[10] + ' 2025');
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26 + Nov_2025_26);
                            //}
                            //else if (MonthId == 12 && yearId == 2025) {
                            //    monthArrCum.push(monthname[3] + ' 2025');
                            //    monthArrCum.push(monthname[4] + ' 2025');
                            //    monthArrCum.push(monthname[5] + ' 2025');
                            //    monthArrCum.push(monthname[6] + ' 2025');
                            //    monthArrCum.push(monthname[7] + ' 2025');
                            //    monthArrCum.push(monthname[8] + ' 2025');
                            //    monthArrCum.push(monthname[9] + ' 2025');
                            //    monthArrCum.push(monthname[10] + ' 2025');
                            //    monthArrCum.push('' + date + ' ' + monthname[11] + ' 2025');
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26 + Nov_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26 + Nov_2025_26 + Dec_2025_26);
                            //}
                            //else if (MonthId == 1 && yearId == 2026) {
                            //    monthArrCum.push(monthname[3] + ' 2025');
                            //    monthArrCum.push(monthname[4] + ' 2025');
                            //    monthArrCum.push(monthname[5] + ' 2025');
                            //    monthArrCum.push(monthname[6] + ' 2025');
                            //    monthArrCum.push(monthname[7] + ' 2025');
                            //    monthArrCum.push(monthname[8] + ' 2025');
                            //    monthArrCum.push(monthname[9] + ' 2025');
                            //    monthArrCum.push(monthname[10] + ' 2025');
                            //    monthArrCum.push(monthname[11] + ' 2025');
                            //    monthArrCum.push('' + date + ' ' + monthname[0] + ' 2026');
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26 + Nov_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26 + Nov_2025_26 + Dec_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26 + Nov_2025_26 + Dec_2025_26 + Jan_2025_26);
                            //}
                            //else if (MonthId == 2 && yearId == 2026) {
                            //    monthArrCum.push(monthname[3] + ' 2025');
                            //    monthArrCum.push(monthname[4] + ' 2025');
                            //    monthArrCum.push(monthname[5] + ' 2025');
                            //    monthArrCum.push(monthname[6] + ' 2025');
                            //    monthArrCum.push(monthname[7] + ' 2025');
                            //    monthArrCum.push(monthname[8] + ' 2025');
                            //    monthArrCum.push(monthname[9] + ' 2025');
                            //    monthArrCum.push(monthname[10] + ' 2025');
                            //    monthArrCum.push(monthname[11] + ' 2025');
                            //    monthArrCum.push(monthname[0] + ' 2026');
                            //    monthArrCum.push('' + date + ' ' + monthname[1] + ' 2026');
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26 + Nov_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26 + Nov_2025_26 + Dec_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26 + Nov_2025_26 + Dec_2025_26 + Jan_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26 + Nov_2025_26 + Dec_2025_26 + Jan_2025_26 + Feb_2025_26);
                            //}
                            //else if (MonthId == 3 && yearId == 2026) {
                            //    monthArrCum.push(monthname[3] + ' 2025');
                            //    monthArrCum.push(monthname[4] + ' 2025');
                            //    monthArrCum.push(monthname[5] + ' 2025');
                            //    monthArrCum.push(monthname[6] + ' 2025');
                            //    monthArrCum.push(monthname[7] + ' 2025');
                            //    monthArrCum.push(monthname[8] + ' 2025');
                            //    monthArrCum.push(monthname[9] + ' 2025');
                            //    monthArrCum.push(monthname[10] + ' 2025');
                            //    monthArrCum.push(monthname[11] + ' 2025');
                            //    monthArrCum.push(monthname[0] + ' 2026');
                            //    monthArrCum.push(monthname[1] + ' 2026');
                            //    monthArrCum.push('' + date + ' ' + monthname[2] + ' 2026');
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26 + Nov_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26 + Nov_2025_26 + Dec_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26 + Nov_2025_26 + Dec_2025_26 + Jan_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26 + Nov_2025_26 + Dec_2025_26 + Jan_2025_26 + Feb_2025_26);
                            //    dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26 + Nov_2025_26 + Dec_2025_26 + Jan_2025_26 + Feb_2025_26 + Mar_2025_26);
                            //}


                            ////*****************************************************  iamsubhash24@gmail.com end    *********************************



                            //*****************************************************  iamsubhash24@gmail.com start   *********************************




                            //----------------2024-2025----DATA BIND
                            monthArrCum.push(monthname[3] + ' 2024');
                            monthArrCum.push(monthname[4] + ' 2024');
                            monthArrCum.push(monthname[5] + ' 2024');
                            monthArrCum.push(monthname[6] + ' 2024');
                            monthArrCum.push(monthname[7] + ' 2024');
                            monthArrCum.push(monthname[8] + ' 2024');
                            monthArrCum.push(monthname[9] + ' 2024');
                            monthArrCum.push(monthname[10] +' 2024');
                            monthArrCum.push(monthname[11] +' 2024');
                            monthArrCum.push(monthname[0] + ' 2025');
                            monthArrCum.push(monthname[1] + ' 2025');
                            monthArrCum.push(monthname[2] + ' 2025');
                            dataArr.push(Total_HC_01042024 + Apr_2024_25);
                            dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25);
                            dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25 + Jun_2024_25);
                            dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25 + Jun_2024_25 + Jul_2024_25);
                            dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25 + Jun_2024_25 + Jul_2024_25 + Aug_2024_25);
                            dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25 + Jun_2024_25 + Jul_2024_25 + Aug_2024_25 + Sep_2024_25);
                            dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25 + Jun_2024_25 + Jul_2024_25 + Aug_2024_25 + Sep_2024_25 + Oct_2024_25);
                            dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25 + Jun_2024_25 + Jul_2024_25 + Aug_2024_25 + Sep_2024_25 + Oct_2024_25 + Nov_2024_25);
                            dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25 + Jun_2024_25 + Jul_2024_25 + Aug_2024_25 + Sep_2024_25 + Oct_2024_25 + Nov_2024_25 + Dec_2024_25);
                            dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25 + Jun_2024_25 + Jul_2024_25 + Aug_2024_25 + Sep_2024_25 + Oct_2024_25 + Nov_2024_25 + Dec_2024_25 + Jan_2024_25);
                            dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25 + Jun_2024_25 + Jul_2024_25 + Aug_2024_25 + Sep_2024_25 + Oct_2024_25 + Nov_2024_25 + Dec_2024_25 + Jan_2024_25 + Feb_2024_25);
                            dataArr.push(Total_HC_01042024 + Apr_2024_25 + May_2024_25 + Jun_2024_25 + Jul_2024_25 + Aug_2024_25 + Sep_2024_25 + Oct_2024_25 + Nov_2024_25 + Dec_2024_25 + Jan_2024_25 + Feb_2024_25 + Mar_2024_25);





                            //----------------2025-2026----DATA BIND
                            monthArrCum.push(monthname[3] + ' 2025');
                            monthArrCum.push(monthname[4] + ' 2025');
                            monthArrCum.push(monthname[5] + ' 2025');
                            monthArrCum.push(monthname[6] + ' 2025');
                            monthArrCum.push(monthname[7] + ' 2025');
                            monthArrCum.push(monthname[8] + ' 2025');
                            monthArrCum.push(monthname[9] + ' 2025');
                            monthArrCum.push(monthname[10]+ ' 2025');
                            monthArrCum.push(monthname[11]+ ' 2025');
                            monthArrCum.push(monthname[0] + ' 2026');
                            monthArrCum.push(monthname[1] + ' 2026');
                            monthArrCum.push(monthname[2] + ' 2026');
                            dataArr.push(Total_HC_01042025 + Apr_2025_26);
                            dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26);
                            dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26);
                            dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26);
                            dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26);
                            dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26);
                            dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26);
                            dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26 + Nov_2025_26);
                            dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26 + Nov_2025_26 + Dec_2025_26);
                            dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26 + Nov_2025_26 + Dec_2025_26 + Jan_2024_25);                                                                                
                            dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26 + Nov_2025_26 + Dec_2025_26 + Jan_2025_26 + Feb_2025_26);                                                                  
                            dataArr.push(Total_HC_01042025 + Apr_2025_26 + May_2025_26 + Jun_2025_26 + Jul_2025_26 + Aug_2025_26 + Sep_2025_26 + Oct_2025_26 + Nov_2025_26 + Dec_2025_26 + Jan_2025_26 + Feb_2025_26 + Mar_2025_26);


                            //----------------2026-2027----DATA BIND
                            if (MonthId == 4 && yearId == 2026) {
                                monthArrCum.push('' + date + ' ' + monthname[3] + ' 2026');
                                dataArr.push(Total_HC_01042026 + Apr_2026_27);
                            }
                            else if (MonthId == 5 && yearId == 2026) {
                                monthArrCum.push(monthname[3] + ' 2026');
                                monthArrCum.push('' + date + ' ' + monthname[4] + ' 2026');
                                dataArr.push(Total_HC_01042026 + Apr_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27);
                            }
                            else if (MonthId == 6 && yearId == 2026) {
                                monthArrCum.push(monthname[3] + ' 2026');
                                monthArrCum.push(monthname[4] + ' 2026');
                                monthArrCum.push('' + date + ' ' + monthname[5] + ' 2026');
                                dataArr.push(Total_HC_01042026 + Apr_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27);
                            }
                            else if (MonthId == 7 && yearId == 2026) {
                                monthArrCum.push(monthname[3] + ' 2026');
                                monthArrCum.push(monthname[4] + ' 2026');
                                monthArrCum.push(monthname[5] + ' 2026');
                                monthArrCum.push('' + date + ' ' + monthname[6] + ' 2026');
                                dataArr.push(Total_HC_01042026 + Apr_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27);
                            }
                            else if (MonthId == 8 && yearId == 2026) {
                                monthArrCum.push(monthname[3] + ' 2026');
                                monthArrCum.push(monthname[4] + ' 2026');
                                monthArrCum.push(monthname[5] + ' 2026');
                                monthArrCum.push(monthname[6] + ' 2026');
                                monthArrCum.push('' + date + ' ' + monthname[7] + ' 2026');
                                dataArr.push(Total_HC_01042026 + Apr_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27);
                            }
                            else if (MonthId == 9 && yearId == 2026) {
                                monthArrCum.push(monthname[3] + ' 2026');
                                monthArrCum.push(monthname[4] + ' 2026');
                                monthArrCum.push(monthname[5] + ' 2026');
                                monthArrCum.push(monthname[6] + ' 2026');
                                monthArrCum.push(monthname[7] + ' 2026');
                                monthArrCum.push('' + date + ' ' + monthname[8] + ' 2026');
                                dataArr.push(Total_HC_01042026 + Apr_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27);
                            }
                            else if (MonthId == 10 && yearId == 2026) {
                                monthArrCum.push(monthname[3] + ' 2026');
                                monthArrCum.push(monthname[4] + ' 2026');
                                monthArrCum.push(monthname[5] + ' 2026');
                                monthArrCum.push(monthname[6] + ' 2026');
                                monthArrCum.push(monthname[7] + ' 2026');
                                monthArrCum.push(monthname[8] + ' 2026');
                                monthArrCum.push('' + date + ' ' + monthname[9] + ' 2026');
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 );
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27);
                            }

                            else if (MonthId == 11 && yearId == 2026) {
                                monthArrCum.push(monthname[3] + ' 2026');
                                monthArrCum.push(monthname[4] + ' 2026');
                                monthArrCum.push(monthname[5] + ' 2026');
                                monthArrCum.push(monthname[6] + ' 2026');
                                monthArrCum.push(monthname[7] + ' 2026');
                                monthArrCum.push(monthname[8] + ' 2026');
                                monthArrCum.push(monthname[9] + ' 2026');
                                monthArrCum.push('' + date + ' ' + monthname[10] + ' 2026');
                                dataArr.push(Total_HC_01042026 + Apr_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27 + Nov_2026_27);
                            }
                            else if (MonthId == 12 && yearId == 2026) {
                                monthArrCum.push(monthname[3] + ' 2026');
                                monthArrCum.push(monthname[4] + ' 2026');
                                monthArrCum.push(monthname[5] + ' 2026');
                                monthArrCum.push(monthname[6] + ' 2026');
                                monthArrCum.push(monthname[7] + ' 2026');
                                monthArrCum.push(monthname[8] + ' 2026');
                                monthArrCum.push(monthname[9] + ' 2026');
                                monthArrCum.push(monthname[10] +' 2026');
                                monthArrCum.push('' + date + ' ' + monthname[11] + ' 2026');
                                dataArr.push(Total_HC_01042026 + Apr_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27 + Nov_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27 + Nov_2026_27 + Dec_2026_27);
                            }
                            else if (MonthId == 1 && yearId == 2027) {
                                monthArrCum.push(monthname[3] + ' 2026');
                                monthArrCum.push(monthname[4] + ' 2026');
                                monthArrCum.push(monthname[5] + ' 2026');
                                monthArrCum.push(monthname[6] + ' 2026');
                                monthArrCum.push(monthname[7] + ' 2026');
                                monthArrCum.push(monthname[8] + ' 2026');
                                monthArrCum.push(monthname[9] + ' 2026');
                                monthArrCum.push(monthname[10]+ ' 2026');
                                monthArrCum.push(monthname[11]+ ' 2026');
                                monthArrCum.push('' + date + ' ' + monthname[0] + ' 2027');
                                dataArr.push(Total_HC_01042026 + Apr_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27 + Nov_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27 + Nov_2026_27 + Dec_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27 + Nov_2026_27 + Dec_2026_27 + Jan_2026_27);
                            }
                            else if (MonthId == 2 && yearId == 2027) {
                                monthArrCum.push(monthname[3] + ' 2026');
                                monthArrCum.push(monthname[4] + ' 2026');
                                monthArrCum.push(monthname[5] + ' 2026');
                                monthArrCum.push(monthname[6] + ' 2026');
                                monthArrCum.push(monthname[7] + ' 2026');
                                monthArrCum.push(monthname[8] + ' 2026');
                                monthArrCum.push(monthname[9] + ' 2026');
                                monthArrCum.push(monthname[10]+ ' 2026');
                                monthArrCum.push(monthname[11]+ ' 2026');
                                monthArrCum.push(monthname[0] + ' 2027');
                                monthArrCum.push('' + date + ' ' + monthname[1] + ' 2027');
                                dataArr.push(Total_HC_01042026 + Apr_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27 + Nov_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27 + Nov_2026_27 + Dec_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27 + Nov_2026_27 + Dec_2026_27 + Jan_2026_27);                                    
                                dataArr.push(Total_HC_01042025 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27 + Nov_2026_27 + Dec_2026_27 + Jan_2026_27 + Feb_2026_27);
                            }
                            else if (MonthId == 3 && yearId == 2027) {
                                monthArrCum.push(monthname[3] + ' 2026');
                                monthArrCum.push(monthname[4] + ' 2026');
                                monthArrCum.push(monthname[5] + ' 2026');
                                monthArrCum.push(monthname[6] + ' 2026');
                                monthArrCum.push(monthname[7] + ' 2026');
                                monthArrCum.push(monthname[8] + ' 2026');
                                monthArrCum.push(monthname[9] + ' 2026');
                                monthArrCum.push(monthname[10]+ ' 2026');
                                monthArrCum.push(monthname[11]+ ' 2026');
                                monthArrCum.push(monthname[0] + ' 2027');
                                monthArrCum.push(monthname[1] + ' 2027');
                                monthArrCum.push('' + date + ' ' + monthname[2] + ' 2027');
                                dataArr.push(Total_HC_01042026 + Apr_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27 + Nov_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27 + Nov_2026_27 + Dec_2026_27);
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27 + Nov_2026_27 + Dec_2026_27 + Jan_2026_27);                       
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27 + Nov_2026_27 + Dec_2026_27 + Jan_2026_27 + Feb_2026_27);          
                                dataArr.push(Total_HC_01042026 + Apr_2026_27 + May_2026_27 + Jun_2026_27 + Jul_2026_27 + Aug_2026_27 + Sep_2026_27 + Oct_2026_27 + Nov_2026_27 + Dec_2026_27 + Jan_2026_27 + Feb_2026_27 + Mar_2026_27);
                            }


                            //*****************************************************  iamsubhash24@gmail.com end    *********************************








                        }
                    }
                    else if (value == 2) {

                        yearArr.push('2019-2020');
                        yearArr.push('2020-2021');
                        yearArr.push('2021-2022');
                        yearArr.push('2022-2023');
                        yearArr.push('2023-2024');
                        yearArr.push('2024-2025');
                        yearArr.push('2025-2026'); // added
                        yearArr.push('2026-2027'); // added
                        dataArr_Y.push(year2019_20_Total);
                        dataArr_Y.push(year2020_21_Total);
                        dataArr_Y.push(year2021_22_Total);
                        dataArr_Y.push(year2022_23_Total);
                        dataArr_Y.push(year2023_24_Total);
                        dataArr_Y.push(year2024_25_Total);
                        dataArr_Y.push(year2025_26_Total); // added
                        dataArr_Y.push(year2026_27_Total); // added
                    }


                    drawchart(monthArrCum, dataArr, monthArr, dataArr_M, yearArr, dataArr_Y, value, Lang);
                }
            });
        }
        fillDashboard_data = function (Cat, SubCat, Param, Stcode, value) {

            if (value == 0) {
                $("#li0").attr('class', '');
                $("#li1").attr('class', '');
                $("#li2").attr('class', '');
                $("#li0").attr('class', 'jjm-bottombar jjm-border-blue');
                $("#li1").attr('class', 'jjm-bottombar jjm-border-gray');
                $("#li2").attr('class', 'jjm-bottombar jjm-border-gray');

                $("#ag0").attr('class', '');
                $("#ag1").attr('class', '');
                $("#ag2").attr('class', '');
                $("#ag0").attr('class', 'list-group-item jjm-text-blue jjm-CoverageButton jjm-small');
                $("#ag1").attr('class', 'list-group-item jjm-text-gray jjm-QualityButton jjm-small');
                $("#ag2").attr('class', 'list-group-item jjm-text-gray jjm-QualityButton jjm-small');
            }
            else if (value == 1) {
                $("#li0").attr('class', '');
                $("#li1").attr('class', '');
                $("#li2").attr('class', '');
                $("#li0").attr('class', 'jjm-bottombar jjm-border-gray');
                $("#li1").attr('class', 'jjm-bottombar jjm-border-blue');
                $("#li2").attr('class', 'jjm-bottombar jjm-border-gray');

                $("#ag0").attr('class', '');
                $("#ag1").attr('class', '');
                $("#ag2").attr('class', '');
                $("#ag0").attr('class', 'list-group-item jjm-text-gray jjm-QualityButton jjm-small');
                $("#ag1").attr('class', 'list-group-item jjm-text-blue jjm-CoverageButton jjm-small');
                $("#ag2").attr('class', 'list-group-item jjm-text-gray jjm-QualityButton jjm-small');
            }
            else if (value == 2) {
                $("#li0").attr('class', '');
                $("#li1").attr('class', '');
                $("#li2").attr('class', '');
                $("#li0").attr('class', 'jjm-bottombar jjm-border-gray');
                $("#li1").attr('class', 'jjm-bottombar jjm-border-gray');
                $("#li2").attr('class', 'jjm-bottombar jjm-border-blue');

                $("#ag0").attr('class', '');
                $("#ag1").attr('class', '');
                $("#ag2").attr('class', '');
                $("#ag0").attr('class', 'list-group-item jjm-text-gray jjm-QualityButton jjm-small');
                $("#ag1").attr('class', 'list-group-item jjm-text-gray jjm-QualityButton jjm-small');
                $("#ag2").attr('class', 'list-group-item jjm-text-blue jjm-CoverageButton jjm-small');
            }
            var obj = {};
            obj.StCode11 = encodeTxt(Stcode);
            obj.Cat = encodeTxt(Cat);
            obj.SubCat = encodeTxt(SubCat);
            obj.Param = encodeTxt(Param);
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/Bind_table_graph',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {

                    StateWiseFHTCTap(data, Cat, SubCat, Param, Stcode, value, Lang);

                }
            });
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/Bind_Fhtc_info',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {
                    Fhtc_info(data, Cat, SubCat, Param, Stcode);
                    setTimeout(function () {
                        $(".se-pre-con").fadeOut('slow')
                        $("#imgLoading").fadeOut('slow')
                    }, 500);
                }
            });
        }


        changeFinanceData = function (evt, finyear) {
            var i, tablinks;
            tablinks = document.getElementsByClassName("tablink");
            for (i = 0; i < tablinks.length; i++) {
                tablinks[i].className = tablinks[i].className.replace(" jjm-light-grey jjm-border-red", "");
            }
            evt.currentTarget.firstElementChild.className += " jjm-light-grey jjm-border-red";

            getStatewise_Financial_info(G_Cat, G_SubCat, G_Param, G_StCode, finyear);
        }
        getStatewise_Financial_info = function (Cat, SubCat, Param, StCode, finyear) {
            var obj_fin = {};
            obj_fin.StCode11 = encodeTxt(StCode);
            obj_fin.Cat = encodeTxt(Cat);
            obj_fin.SubCat = encodeTxt(SubCat);
            obj_fin.Param = encodeTxt(Param);
            obj_fin.FinYear = encodeTxt(finyear);
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/Bind_BudjectSanction_Details',
                data: JSON.stringify(obj_fin),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (result) {
                    var data = result.d;
                    var total_amount = 0;
                    var tr = "";
                    for (var i = 0; i < data.length; i++) {
                        tr += '<tr class="item">';
                        if (Lang == 'hi') {
                            tr += '<td class="jjm-left-align jjm-tableleftpadding"><div class="jjm-col l12 m12 s12"><a href="javascript:getStateClick(' + "'" + Cat + "'" + ',' + "'" + SubCat + "'" + ',' + "'" + Param + "'" + ',' + "'" + data[i].KeyValue + "'" + ',' + "'" + toTitleCase(data[i].Name_hi) + "'" + ')" style="text-decoration: none;">' + toTitleCase(data[i].Name_hi) + '</a></div></td>';
                        }
                        else {
                            tr += '<td class="jjm-left-align jjm-tableleftpadding "><div class="jjm-col l12 m12 s12"><a href="javascript:getStateClick(' + "'" + Cat + "'" + ',' + "'" + SubCat + "'" + ',' + "'" + Param + "'" + ',' + "'" + data[i].KeyValue + "'" + ',' + "'" + toTitleCase(data[i].Name) + "'" + ')" style="text-decoration: none;">' + toTitleCase(data[i].Name) + '</a></div></td>';
                        }

                        tr += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">' + numberWithCommas(data[i].Amount, 0, 0) + '</div></td>';
                        //tr += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">' + numberWithCommas(data[i].Village_Certified, 0, 0) + '</div></td>';

                        tr += '<td class="jjm-hide">' + data[i].Amount + '</td>';

                        tr += '</tr>';
                        total_amount += parseFloat(data[i].Amount);
                    }

                    var table_Header_desc;
                    if (Lang == 'en') {
                        table_Header_desc = Table_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
                    }
                    else {
                        table_Header_desc = Table_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
                    }
                    var tr_foot = '';
                    tr_foot += '<tr style="font-weight:600;" class="jjm-light-gray">';
                    tr_foot += '<td class="jjm-left-align jjm-tableleftpadding "><div class="jjm-col l12 m12 s12">' + table_Header_desc[0].desc_foot_total + '</div></td>';
                    tr_foot += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">' + numberWithCommas(parseFloat(total_amount), 0, 0) + '</div></td>';
                    tr_foot += '</tr>';

                    $("#tblBody_financial").html("");
                    $("#tblBody_financial").append(tr);

                    $("#tblFoot_financial").html("");
                    $("#tblFoot_financial").append(tr_foot);

                    $("#tblBody_financial_M").html("");
                    $("#tblBody_financial_M").append(tr);

                    $("#tblFoot_financial_M").html("");
                    $("#tblFoot_financial_M").append(tr_foot);
                }
            });
        }
        getBudgetSanction_data = function (Cat, SubCat, Param, Stcode) {
            var graph_HeaderDesc;
            if (Lang == 'hi') {
                graph_HeaderDesc = Graph_HeaderDesc_hi['Cat0']['SubCat0']['Param0'];
            }
            else {
                graph_HeaderDesc = Graph_HeaderDesc['Cat0']['SubCat0']['Param0'];
            }

            var obj = {};
            obj.StCode11 = encodeTxt(G_StCode);
            obj.Cat = encodeTxt(G_Cat);
            obj.SubCat = encodeTxt(G_SubCat);
            obj.Param = encodeTxt(G_Param);
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/Bind_BudgetSanction_info',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {

                    yearArr = [];
                    dataArr_Y = [];

                    for (var i = 0; i < data.d.length; i++) {
                        yearArr.push(data.d[i].FinYear);
                        dataArr_Y.push(parseInt(data.d[i].Amount));
                    }

                    budjectsaction_chart(yearArr, dataArr_Y, Lang);
                }
            });
        }

        getfillDashboard_Graph_data = function (value) {

            //$(".se-pre-con").fadeIn("slow");
            //$("#imgLoading").fadeIn("slow");
            var obj = {};
            obj.StCode11 = encodeTxt(G_StCode);
            obj.Cat = encodeTxt(G_Cat);
            obj.SubCat = encodeTxt(G_SubCat);
            obj.Param = encodeTxt(G_Param);
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/Bind_table_graph',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {
                    stateArr = [];
                    baseline010419_Arr = [];
                    baseline010420_Arr = [];
                    current20_21_Arr = [];
                    remainArr = [];
                    achiveArr = [];

                    remain_15082019_Arr = [];
                    achive_15082019_Arr = [];
                    achive_M_Arr = [];
                    var grapharray = data.d;
                    grapharray = sortByKeyAsc(grapharray, "Per_HC_Remain", true);
                    for (var i = 0; i < grapharray.length; i++) {
                        if (Lang == 'hi') {
                            stateArr.push(grapharray[i].Name_hi);
                        }
                        else {
                            stateArr.push(toTitleCase(grapharray[i].Name));
                        }
                        baseline010419_Arr.push(parseFloat(grapharray[i].Per_HCPWS_01042019));
                        baseline010420_Arr.push(parseFloat(grapharray[i].Per_HCPWS_19_20));
                        current20_21_Arr.push(parseFloat(grapharray[i].Per_HCPWS_20_21));

                        remainArr.push(parseFloat(grapharray[i].HC_Remain));
                        var colorId = data.d[i].ColorId;
                        achiveArr.push(
                            { y: parseFloat(grapharray[i].Value), color: getColorTable(G_Cat, G_SubCat, G_Param, colorId, G_StCode) }
                        )
                        achive_M_Arr.push(
                            { y: parseFloat(grapharray[i].HCPWS_20_21), color: '#ffff00' }
                        )
                        var remain_15082019 = parseFloat(grapharray[i].Total) - parseFloat(data.d[i].HCPWS_01042019);

                        remain_15082019_Arr.push(parseFloat(remain_15082019));
                        achive_15082019_Arr.push(
                            { y: parseFloat(grapharray[i].HCPWS_01042019), color: getColorTable(G_Cat, G_SubCat, G_Param, colorId, G_StCode) }
                        )
                    }

                    FHTC_Chart(stateArr, baseline010419_Arr, baseline010420_Arr, current20_21_Arr, achiveArr, remainArr, remain_15082019_Arr, achive_15082019_Arr, value, Lang, achive_M_Arr)
                    //setTimeout(function () {
                    //    $(".se-pre-con").fadeOut('slow')
                    //    $("#imgLoading").fadeOut('slow')
                    //}, 50);
                }
            });
        }
        fillColorState = function (stateinfo, Cat, SubCat, Param, Stcode) {
            var themeId = localStorage.getItem("themeId");
            if (themeId == 0) {
                statesColor = stboundry_S['Cat' + Cat]['SubCat' + SubCat]['Param' + Param][0]['color'];
            }
            else {
                statesColor = stboundry_S['Cat' + Cat]['SubCat' + SubCat]['Param' + Param][0]['color' + themeId];
            }
            stateLayer.show();
            var renderer = new UniqueValueRenderer(defaultSymbol, "STCODE11");
            var pointsRenderer = new UniqueValueRenderer(null, "STCODE11");
            for (var i = 0; i < stateinfo.length; i++) {
                var colorId = stateinfo[i].ColorId;
                if (stateinfo[i].KeyValue == "31") {
                    renderer.addValue(stateinfo[i].KeyValue, new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), 4.0), new Color(getColor(Cat, SubCat, Param, colorId, Stcode))));
                }
                else {
                    renderer.addValue(stateinfo[i].KeyValue, new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), stLayerWidth), new Color(getColor(Cat, SubCat, Param, colorId, Stcode))));
                }
                if (parseInt(stateinfo[i].IsHGJCertified) >= 1) {
                    var symbol = new PictureMarkerSymbol({
                        "url": "content/images/hgj_star.png",
                        "height": 12,
                        "width": 12,
                        "type": "esriPMS",
                        /*"angle": 120,*/
                        "xoffset": 0,
                        "yoffset": 0,
                        "outline": { "color": [0, 0, 0, 1], "width": 1, "type": "esriSLS", "style": "esriSLSSolid" }
                    });
                    pointsRenderer.addValue(stateinfo[i].KeyValue, symbol);
                }
                else if (parseInt(stateinfo[i].IsHGJCertified) == 0 && parseInt(stateinfo[i].ISHGJReported) >= 1) {
                    var symbol_reported = new PictureMarkerSymbol({
                        "url": "content/images/hgj_star_reported.png",
                        "height": 12,
                        "width": 12,
                        "type": "esriPMS",
                        /*"angle": 90,*/
                        "xoffset": 0,
                        "yoffset": 0,
                        "outline": { "color": [0, 0, 0, 1], "width": 1, "type": "esriSLS", "style": "esriSLSSolid" }
                    });
                    pointsRenderer.addValue(stateinfo[i].KeyValue, symbol_reported);
                }
            }
            //stateHGJpointLayer
            stateLayer.setRenderer(renderer);
            stateLayer.redraw();
            stateBoundry.hide();
            stateHGJpointLayer.setRenderer(pointsRenderer);
            if (SubCat == "1") {
                stateHGJpointLayer.hide();
            }
            else {
                stateHGJpointLayer.show();
            }
            map.addLayers([districtLayer, stateLayer, stateHGJpointLayer]);
            districtLayer.hide();
            legendMap(Cat, SubCat, Param, G_StCode);
        }
        fillColorStateByStateId = function (stateinfo, Cat, SubCat, Param, Stcode) {
            stateLayer.show();
            var renderer = new UniqueValueRenderer(defaultSymbol, "STCODE11");
            for (var i = 0; i < stateinfo.length; i++) {
                var colorId = stateinfo[i].ColorId;
                if (Stcode == stateinfo[i].KeyValue) {
                    renderer.addValue(stateinfo[i].KeyValue, new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), stLayerWidth), new Color(getColor(Cat, SubCat, Param, colorId, Stcode))));
                }
            }
            stateLayer.setRenderer(renderer);
            stateLayer.redraw();
            stateBoundry.hide();
            map.addLayers([districtLayer, stateLayer]);
            districtLayer.hide();
        }
        fillColorDistrict = function (stateinfo, Cat, SubCat, Param, stcode) {

            var themeId = localStorage.getItem("themeId");
            if (themeId == 0) {
                districtsColor = stboundry_D['Cat' + Cat]['SubCat' + SubCat]['Param' + Param][0]['color'];
            }
            else {
                districtsColor = stboundry_D['Cat' + Cat]['SubCat' + SubCat]['Param' + Param][0]['color' + themeId];
            }
            districtLayer.show();

            var stfont = new Font("11px", Font.STYLE_NORMAL, Font.VARIANT_SMALLCAPS, Font.WEIGHT_BOLD, "Arial");
            stPointlayer.clear();
            var renderer = new UniqueValueRenderer(defaultSymbol, "dtcode11");
            for (var i = 0; i < stateinfo.length; i++) {
                var colorId = stateinfo[i].ColorId;
                renderer.addValue(stateinfo[i].KeyValue, new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(districtsColor), dtLayerWidth), new Color(getColor(Cat, SubCat, Param, colorId, stcode))));
            }

            districtLayer.setRenderer(renderer);
            districtLayer.redraw();
            districtLayer.show();
            var labelClass;
            if (stcode == "0") {
                stPointlayer.show();
                for (var i = 0; i < StPoint.length; i++) {
                    var stPoint = new Point([StPoint[i].Long, StPoint[i].Lat]);
                    stPoint = esri.geometry.geographicToWebMercator(stPoint);
                    var textSymbol = new TextSymbol(StPoint[i].Name, stfont, new Color([0, 0, 0]));
                    var attributes = {
                        KeyValue: StPoint[i].KeyValue,
                        KeyId: StPoint[i].KeyId
                    };
                    var stPointGraphicText = new esri.Graphic(stPoint, textSymbol, attributes);
                    stPointlayer.redraw();
                    stPointlayer.add(stPointGraphicText);
                }
                //map.addLayer(stPointlayer);
                stateBoundry.show();
                StateColor();
                labelClass = new esri.layers.LabelClass({
                    labelExpression: '[dtname]',
                    labelPlacement: 'always-horizontal',
                    symbol: new esri.symbol.TextSymbol()
                    //minScale: 9244648.869//display village name on map after this scale value
                });
                labelClass.symbol = new TextSymbol({
                    font: new Font("0px", Font.STYLE_NORMAL, Font.VARIANT_NORMAL, Font.WEIGHT_BOLD, "Arial"),
                    color: new Color("#000000")
                });
            }
            else {
                StateOtherColor(stcode);
                stateBoundry.hide();
                labelClass = new esri.layers.LabelClass({
                    labelExpression: '[dtname]',
                    labelPlacement: 'always-horizontal',
                    where: "stcode11 = '" + stcode + "'", // filter district wise village name
                    symbol: new esri.symbol.TextSymbol()
                    //minScale: 9244648.869//display village name on map after this scale value
                });
                labelClass.symbol = new TextSymbol({
                    font: new Font("9px", Font.STYLE_NORMAL, Font.VARIANT_NORMAL, Font.WEIGHT_BOLD, "Arial"),
                    color: new Color("#000000")
                });
            }
            districtLayer.setLabelingInfo([labelClass]);
            districtLayer.redraw();
            stateLayer.show();
            stateHGJpointLayer.hide();
            map.addLayers([districtLayer, stateBoundry]);

            legendMap(Cat, SubCat, Param, G_StCode);
        }
        var highlightSymbol = new SimpleFillSymbol(
            SimpleFillSymbol.STYLE_SOLID,
            new SimpleLineSymbol(
                SimpleLineSymbol.STYLE_SOLID,
                new Color([245, 246, 32]), 1
            ),
            new Color([125, 125, 125, 0.35])
        );

        function toTitleCase(str) {
            if (str == 'D&NH and D&D') {
                return str;
            }
            else {
                return str.replace(/\w\S*/g, function (txt) { return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase(); });
            }
        }
        ChangeMap(Cat, SubCat, Param);
        //close the dialog when the mouse leaves the highlight graphic
        var graphic;
        var layer;
        var data;
        var count = 0;
        var countPie = 0;
        layer = new esri.layers.GraphicsLayer();
        map.on("extent-change", showExtent);

        function showExtent(event) {
            //console.log("Map extent-change", JSON.stringify(event.extent));

            var innerContent;
            var extent = webMercatorUtils.webMercatorToGeographic(event.extent);
            innerContent = "XMin: " + event.extent.xmin.toFixed(2) + "&nbsp;" +
                "YMin: " + event.extent.ymin.toFixed(2) + "&nbsp;" +
                "XMax: " + event.extent.xmax.toFixed(2) + "&nbsp;" +
                "YMax: " + event.extent.ymax.toFixed(2);
        }
        map.on("load", function () {
            map.infoWindow.resize(245, 180);
            map.disableScrollWheelZoom();
            map.disableDoubleClickZoom();
            map.disableMapNavigation();
            map.disableRubberBandZoom();
            map.disablePan();
            map.disableKeyboardNavigation();
            map.disableShiftDoubleClickZoom();
            map.graphics.enableMouseEvents();
            map.graphics.on("mouse-out", closeDialog);
            //$("#map svg").css("touch-action", "block");

            document.querySelector('#map #map_container').setAttribute("style", "position: absolute; cursor: default; touch-action: block; clip: auto;");
            document.querySelector('#map svg').setAttribute("style", "touch-action: block; will-change: transform; overflow: visible; position: absolute;");
        });

        function encodeTxt(s) {
            //console.log(encN);
            s = escape(s);
            var ta = new Array();
            for (i = 0; i < s.length; i++) ta[i] = s.charCodeAt(i) + encN;
            return "" + escape(eval("String.fromCharCode(" + ta + ")")) + encN;
        }

        function closeDialog() {
            map.graphics.clear();
            map.setMapCursor("default");
            map.infoWindow.hide();
        }
        var highlightSymbol1 = new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID,
            new Color([0, 0, 0]), 1), new Color([0, 0, 0, 0]));

        dojo.connect(stateLayer, "onClick", onStateClick);

        function onStateClick(evt) {
            if (G_SubCat == "0") {
                var stname = esriLang.substitute(evt.graphic.attributes, '${STNAME}');
                var stcode11 = esriLang.substitute(evt.graphic.attributes, '${STCODE11}');
                G_StCode = stcode11;
                G_StName = stname;

                getStateClick(G_Cat, "0", G_Param, G_StCode, G_StName);
            }
            //getdataStateClickAsondate(G_Cat, "1", G_Param, G_StCode, G_StName);
        };
        getStateClick = function (G_Cat, G_SubCat, G_Param, stcode11, G_StName) {
            sessionStorage.setItem("G_Cat", G_Cat);
            sessionStorage.setItem("G_SubCat", G_SubCat);
            sessionStorage.setItem("G_Param", G_Param);
            sessionStorage.setItem("G_StCode", stcode11);
            sessionStorage.setItem("G_StName", G_StName);
            sessionStorage.setItem("Lang", Lang);
            window.location.href = "JJMState.aspx";

        }
        StateOtherColor = function (stcode11) {

            var statesColor = new Color('#000000');
            var renderer = new UniqueValueRenderer(defaultSymbol, "STCODE11");
            var statesRenderer = new UniqueValueRenderer(defaultSymbol, "STCODE11");
            //add symbol for each possible value

            var stColor = [255, 255, 255, 0.1];
            if (stcode11 == "01") {
                renderer.addValue(stcode11, new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), stLayerWidth), new Color(jkColor)));
            }
            else {
                renderer.addValue(stcode11, new SimpleFillSymbol(SimpleFillSymbol.STYLE_SOLID, new SimpleLineSymbol(SimpleLineSymbol.STYLE_SOLID, new Color(statesColor), stLayerWidth), new Color(stColor)));
            }
            stateLayer.setRenderer(renderer);
            stateLayer.redraw();
            stateBoundry.redraw();
            stateBoundry.setRenderer(statesRenderer);
            stateBoundry.hide();
        }

        function getColor(cat, subcat, param, legendIdx, stcode) {
            try {
                var themeId = localStorage.getItem("themeId")
                if (typeof (themeId) == "undefined" || themeId == null) {
                    themeId = 0;
                }
                if (stcode == "0") {
                    if (themeId == 0) {
                        return legends_S['Cat' + cat]['SubCat' + subcat]['Param' + param][legendIdx]['color'];
                    }
                    else {
                        return legends_S['Cat' + cat]['SubCat' + subcat]['Param' + param][legendIdx]['color' + themeId];
                    }
                }
                else {
                    if (themeId == 0) {
                        return legends_D['Cat' + cat]['SubCat' + subcat]['Param' + param][legendIdx]['color'];
                    }
                    else {
                        return legends_D['Cat' + cat]['SubCat' + subcat]['Param' + param][legendIdx]['color' + themeId];
                    }

                }

            } catch (e) {
                return 'rgba(255,255,255,0)';
            }
        }
        function getColor_graph(cat, subcat, param, legendIdx, stcode) {
            try {
                if (stcode == "0") {
                    return legend_Graph_HC['Cat' + cat]['SubCat' + subcat]['Param' + param][legendIdx]['color'];
                }
                else {
                    return legend_Graph_HC['Cat' + cat]['SubCat' + subcat]['Param' + param][legendIdx]['color'];
                }

            } catch (e) {
                return 'rgba(255,255,255,0)';
            }
        }
        function getCurrentDate() {
            var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
            ];

            var today = new Date();
            var dd = today.getDate();
            var mm = today.getMonth() + 1; //January is 0!
            var yyyy = today.getFullYear();

            if (dd < 10) {
                dd = '0' + dd;
            }
            if (mm < 10) {
                mm = '0' + mm;
            }
            var today = dd + ' ' + monthNames[today.getMonth()] + ' ' + yyyy;
            //var today = dd + '/' + mm + '/' + yyyy;
            return today;
        }
        function getCurrentDate_hi() {
            var monthNames = ["जनवरी", "फ़रवरी", "मार्च", "अप्रैल", "मई", "जून",
                "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसम्बर"
            ];

            var today = new Date();
            var dd = today.getDate();
            var mm = today.getMonth() + 1; //January is 0!
            var yyyy = today.getFullYear();

            if (dd < 10) {
                dd = '0' + dd;
            }
            if (mm < 10) {
                mm = '0' + mm;
            }
            var today = dd + ' ' + monthNames[today.getMonth()] + ' ' + yyyy;
            //var today = dd + '/' + mm + '/' + yyyy;
            return today;
        }
        function legendMap(cat, subcat, param, stcode) {
            var legend;
            if (stcode == "0") {
                legend = legends_S['Cat' + cat]['SubCat' + subcat]['Param' + param];
            }
            else {
                legend = legends_D['Cat' + cat]['SubCat' + subcat]['Param' + param];
            }
            $('#legend').show();
            $("#legend li").remove();
            var themeId = localStorage.getItem("themeId");
            if (typeof (themeId) == "undefined" || themeId == null) {
                themeId = 0;
            }
            if (param == 0) {
                for (i = 0; i < legend.length; i++) {
                    if (i == 4) {
                        if (themeId == 0) {
                            $("#legend ul").append('<li style="width:' + parseInt((100 / legend.length)) + '%;padding:1px;"><span class="jjm-small"><font style="color:rgba(0, 0, 0, 1)">' + legend[i].desc + '</font></span><span style="height: 10px; background:' + legend[i].color + ';"></span></li>');
                        }
                        else if (themeId == 1) {
                            $("#legend ul").append('<li style="width:' + parseInt((100 / legend.length)) + '%;padding:1px;"><span class="jjm-small"><font style="color:rgba(160, 219, 253, 1)">' + legend[i].desc + '</font></span><span style="height: 10px; background:' + legend[i].color1 + ';"></span></li>');
                        }
                        else if (themeId == 2) {
                            $("#legend ul").append('<li style="width:' + parseInt((100 / legend.length)) + '%;padding:1px;"><span class="jjm-small"><font style="color:rgba(160, 219, 253, 1)">' + legend[i].desc + '</font></span><span style="height: 10px; background:' + legend[i].color1 + ';"></span></li>');
                        }
                    }
                    else {
                        if (themeId == 0) {
                            $("#legend ul").append('<li style="width:' + parseInt((100 / legend.length)) + '%;padding:1px;"><span class="jjm-small"><font style="color:rgba(0, 0, 0, 1)">' + legend[i].desc + '</font></span><span style="height: 10px; background:' + legend[i].color + ';"></span></li>');
                        }
                        else if (themeId == 1) {
                            $("#legend ul").append('<li style="width:' + parseInt((100 / legend.length)) + '%;padding:1px;"><span class="jjm-small"><font style="color:rgba(160, 219, 253, 1)">' + legend[i].desc + '</font></span><span style="height: 10px; background:' + legend[i].color1 + ';"></span></li>');
                        }
                        else if (themeId == 2) {
                            $("#legend ul").append('<li style="width:' + parseInt((100 / legend.length)) + '%;padding:1px;"><span class="jjm-small"><font style="color:rgba(160, 219, 253, 1)">' + legend[i].desc + '</font></span><span style="height: 10px; background:' + legend[i].color1 + ';"></span></li>');
                        }
                    }
                }
            }
            else {
                for (i = 0; i < legend.length; i++) {
                    if (i == 4) {
                        if (themeId == 0) {
                            $("#legend ul").append('<li style="width:' + parseInt((100 / legend.length)) + '%;padding:1px;"><span class="jjm-small"><font style="color:rgba(0, 0, 0, 1)">' + legend[i].desc + '</font></span><span style="height: 10px; background:' + legend[i].color + ';"></span></li>');
                        }
                        else if (themeId == 1) {
                            $("#legend ul").append('<li style="width:' + parseInt((100 / legend.length)) + '%;padding:1px;"><span class="jjm-small"><font style="color:rgba(160, 219, 253, 1)">' + legend[i].desc + '</font></span><span style="height: 10px; background:' + legend[i].color1 + ';"></span></li>');
                        }
                        else if (themeId == 2) {
                            $("#legend ul").append('<li style="width:' + parseInt((100 / legend.length)) + '%;padding:1px;"><span  class="jjm-small"><font style="color:rgba(160, 219, 253, 1)">' + legend[i].desc + '</font></span><span style="height: 10px; background:' + legend[i].color1 + ';"></span></li>');
                        }
                    }
                    else {
                        if (themeId == 0) {
                            $("#legend ul").append('<li style="width:' + parseInt((100 / legend.length)) + '%;padding:1px;"><span class="jjm-small"><font style="color:rgba(0, 0, 0, 1)">' + legend[i].desc + '</font></span><span style="height: 10px; background:' + legend[i].color + ';"></span></li>');
                        }
                        else if (themeId == 1) {
                            $("#legend ul").append('<li style="width:' + parseInt((100 / legend.length)) + '%;padding:1px;"><span class="jjm-small"><font style="color:rgba(160, 219, 253, 1)">' + legend[i].desc + '</font></span><span style="height: 10px; background:' + legend[i].color1 + ';"></span></li>');
                        }
                        else if (themeId == 2) {
                            $("#legend ul").append('<li style="width:' + parseInt((100 / legend.length)) + '%;padding:1px;"><span  class="jjm-small"><font style="color:rgba(160, 219, 253, 1)">' + legend[i].desc + '</font></span><span style="height: 10px; background:' + legend[i].color1 + ';"></span></li>');
                        }
                    }
                }
            }
        }

        displayFhtc_info_Status_data = function (value) {
            $("#Popup_FhtcStatus").show();
            if (value == 0) {
                $("#FHTC_Chart_District").show();
                $("#FHTC_Chart_Block").hide();
                $("#FHTC_Chart_Panchayat").hide();
                $("#FHTC_Chart_Village").hide();
                $("#lblfhtc_status").text("100 % FHTC Districts");
            }
            else if (value == 1) {
                $("#FHTC_Chart_District").hide();
                $("#FHTC_Chart_Block").show();
                $("#FHTC_Chart_Panchayat").hide();
                $("#FHTC_Chart_Village").hide();
                $("#lblfhtc_status").text("100 % FHTC Blocks");
            }
            else if (value == 2) {
                $("#FHTC_Chart_District").hide();
                $("#FHTC_Chart_Block").hide();
                $("#FHTC_Chart_Panchayat").show();
                $("#FHTC_Chart_Village").hide();
                $("#lblfhtc_status").text("100 % FHTC Panchayts");
            }
            else if (value == 3) {
                $("#FHTC_Chart_District").hide();
                $("#FHTC_Chart_Block").hide();
                $("#FHTC_Chart_Panchayat").hide();
                $("#FHTC_Chart_Village").show();
                $("#lblfhtc_status").text("100 % FHTC Villages");
            }
        }
        //============ search------
        getdataVillageClick = function (stcode, dtcode, villcode, villageId, stname, dtname, vname) {
            sessionStorage.setItem("G_Cat", G_Cat);
            sessionStorage.setItem("G_SubCat", G_SubCat);
            sessionStorage.setItem("G_Param", G_Param);
            sessionStorage.setItem("G_StCode", stcode);
            sessionStorage.setItem("G_DtCode", dtcode);
            sessionStorage.setItem("G_StName", stname);
            sessionStorage.setItem("G_DtName", dtname);
            sessionStorage.setItem("G_VillCode", villcode);
            sessionStorage.setItem("G_VillName", vname);
            sessionStorage.setItem("G_VillId", villageId);
            sessionStorage.setItem("Lang", Lang);
            sessionStorage.setItem("Prv_PageName", "JJMIndia.aspx");
            window.location.href = "JJMVillage_Profile.aspx";

        }

        getdataStateClick = function (KeyId, KeyValue, KeyName) {
            $("#lblStateCode").text(KeyValue);
            $("#lblStateName").text(KeyName);
            //var tr_Search = '';
            //tr_Search += '<thead><tr>';
            //tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + KeyName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="removeStateSearch()"></i></div></th><tr>';
            //tr_Search += ' </tr> </thead>';
            //tr_Search += '<tbody>';
            //tr_Search += '<td class="jjm-left-align jjm-border-top" style="width:100%;"></td>';
            //tr_Search += '</tr>';
            //tr_Search += '</tbody>';
            //$("#tbl_search").html("");
            //$("#tbl_search").append(tr_Search);
            //$("#tbl_search").show();
            ////$("#myInput").attr("placeholder", "Search district ...");
            //$('#myInput').val('');
            getStateDistrict();
        }
        getdataDistrictClick = function (KeyId, KeyValue, KeyName) {
            $("#lblDistrictCode").text(KeyValue);
            $("#lblDistrictName").text(KeyName);
            var StName = $("#lblStateName").text();

            var tr_Search = '';
            tr_Search += '<thead><tr>';
            tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + StName + '</label></div><div class="jjm-padding-small jjm-border jjm-light-gray jjm-border-green jjm-card-2 jjm-round-large" style="margin-left: 6px !important;display:inline-block;"><label class="jjm-medium">' + KeyName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="removeDistrictSearch()"></i></div></th></tr>';
            tr_Search += '<tr><th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>To search a village type first few letters of name of the village</b></th>';
            tr_Search += ' </tr> </thead>';
            tr_Search += '<tbody>';
            tr_Search += '<td class="jjm-left-align jjm-border-top" style="width:100%;"></td>';
            tr_Search += '</tr>';
            tr_Search += '</tbody>';
            $("#tbl_search").html("");
            $("#tbl_search").append(tr_Search);
            $("#tbl_search").show();
            //$("#myInput").attr("placeholder", "Search village ...");
            $('#myInput').val('');
        }
        removeDistrictSearch = function () {
            $('#myInput').val('');
            var StCode = $("#lblStateCode").text();
            var StName = $("#lblStateName").text();

            $("#lblDistrictCode").text('0');
            $("#lblDistrictName").text('');
            var tr_Search = '';
            var obj = {};
            obj.StCode = encodeTxt(StCode);
            obj.Name = encodeTxt('');
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/JJM_StateDistrictSearch',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {
                    if (StCode == '0' || StCode == '') {
                        //$("#myInput").attr("placeholder", "Search state ...");
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your state</b><i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="closetable()"></i></th>';
                        tr_Search += ' </tr> </thead>';
                    }
                    else {
                        //$("#myInput").attr("placeholder", "Search district ...");
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + StName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="removeStateSearch()"></i></div></th><tr>';
                        tr_Search += '<tr><th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your district</b></th>';
                        tr_Search += ' </tr> </thead>';
                    }

                    tr_Search += '<tbody><tr><td>';
                    for (var i = 0; i < data.d.length; i++) {
                        if (StCode == '0' || StCode == '') {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataStateClick(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        else {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataDistrictClick(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        tr_Search += '' + toTitleCase(data.d[i].KeyName) + '</div>';
                    }
                    tr_Search += '</td></tr></tbody>';
                    $("#tbl_search").html("");
                    $("#tbl_search").append(tr_Search);
                    $("#tbl_search").show();
                }
            });
        }

        removeStateSearch = function () {
            $("#lblStateCode").text('0');
            $("#lblStateName").text('');

            $("#lblDistrictCode").text('0');
            $("#lblDistrictName").text('');

            $('#myInput').val('');


            var StCode = $("#lblStateCode").text();
            var StName = $("#lblStateName").text();
            var tr_Search = '';
            var obj = {};
            obj.StCode = encodeTxt(StCode);
            obj.Name = encodeTxt('');
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/JJM_StateDistrictSearch',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {
                    if (StCode == '0' || StCode == '') {
                        //$("#myInput").attr("placeholder", "Search state ...");
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your state</b><i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="closetable()"></i></th>';
                        tr_Search += ' </tr> </thead>';
                    }
                    else {
                        //$("#myInput").attr("placeholder", "Search district ...");
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + StName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="removeStateSearch()"></i></div></th><tr>';
                        tr_Search += '<tr><th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your district</b></th>';
                        tr_Search += ' </tr> </thead>';
                    }

                    tr_Search += '<tbody><tr><td>';
                    for (var i = 0; i < data.d.length; i++) {
                        if (StCode == '0' || StCode == '') {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataStateClick(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';

                        }
                        else {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataDistrictClick(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        tr_Search += '' + toTitleCase(data.d[i].KeyName) + '</div>';
                    }
                    tr_Search += '</td></tr></tbody>';
                    $("#tbl_search").html("");
                    $("#tbl_search").append(tr_Search);
                    $("#tbl_search").show();
                }
            });
        }

        closetable = function () {
            $("#lblStateCode").text('0');
            $("#lblStateName").text('');
            $("#lblDistrictCode").text('0');
            $("#lblDistrictName").text('');

            $('#myInput').val('');
            $('#myInput_M').val('');
            $("#tbl_search").html("");
            $("#tbl_search").append('');
            $("#tbl_search").hide();
            $("#tbl_search_M").html("");
            $("#tbl_search_M").append('');
            $("#tbl_search_M").hide();
        }


        //============Mobile search------

        getdataStateClick_M = function (KeyId, KeyValue, KeyName) {
            $("#lblStateCode").text(KeyValue);
            $("#lblStateName").text(KeyName);
            //var tr_Search = '';
            //tr_Search += '<thead><tr>';
            //tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + KeyName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="removeStateSearch_M()"></i></div></th><tr>';
            //tr_Search += ' </tr> </thead>';
            //tr_Search += '<tbody>';
            //tr_Search += '<td class="jjm-left-align jjm-border-top" style="width:100%;"></td>';
            //tr_Search += '</tr>';
            //tr_Search += '</tbody>';
            //$("#tbl_search_M").html("");
            //$("#tbl_search_M").append(tr_Search);
            //$("#tbl_search_M").show();
            ////$("#myInput").attr("placeholder", "Search district ...");
            //$('#myInput_M').val('');
            getStateDistrict_M();
        }
        getdataDistrictClick_M = function (KeyId, KeyValue, KeyName) {
            $("#lblDistrictCode").text(KeyValue);
            $("#lblDistrictName").text(KeyName);
            var StName = $("#lblStateName").text();

            var tr_Search = '';
            tr_Search += '<thead><tr>';
            tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + StName + '</label></div><div class="jjm-padding-small jjm-border jjm-light-gray jjm-border-green jjm-card-2 jjm-round-large" style="margin-left: 6px !important;display:inline-block;"><label class="jjm-medium">' + KeyName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="removeDistrictSearch_M()"></i></div></th></tr>';
            tr_Search += '<tr><th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>To search a village type first few letters of name of the village</b></th>';
            tr_Search += ' </tr> </thead>';
            tr_Search += '<tbody>';
            tr_Search += '<td class="jjm-left-align jjm-border-top" style="width:100%;"></td>';
            tr_Search += '</tr>';
            tr_Search += '</tbody>';
            $("#tbl_search_M").html("");
            $("#tbl_search_M").append(tr_Search);
            $("#tbl_search_M").show();
            //$("#myInput").attr("placeholder", "Search village ...");
            $('#myInput_M').val('');
        }

        removeDistrictSearch_M = function () {
            $('#myInput_M').val('');
            var StCode = $("#lblStateCode").text();
            var StName = $("#lblStateName").text();
            $("#lblDistrictCode").text('0');
            $("#lblDistrictName").text('');

            var tr_Search = '';
            var obj = {};
            obj.StCode = encodeTxt(StCode);
            obj.Name = encodeTxt('');
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/JJM_StateDistrictSearch',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {
                    if (StCode == '0' || StCode == '') {
                        //$("#myInput").attr("placeholder", "Search state ...");
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your state</b><i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="closetable()"></i></th>';
                        tr_Search += ' </tr> </thead>';
                    }
                    else {
                        //$("#myInput").attr("placeholder", "Search district ...");
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + StName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="removeStateSearch_M()"></i></div></th><tr>';
                        tr_Search += '<tr><th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your district</b></th>';
                        tr_Search += ' </tr> </thead>';
                    }

                    tr_Search += '<tbody><tr><td>';
                    for (var i = 0; i < data.d.length; i++) {
                        if (StCode == '0' || StCode == '') {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataStateClick_M(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        else {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataDistrictClick_M(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        tr_Search += '' + toTitleCase(data.d[i].KeyName) + '</div>';
                    }
                    tr_Search += '</td></tr></tbody>';
                    $("#tbl_search_M").html("");
                    $("#tbl_search_M").append(tr_Search);
                    $("#tbl_search_M").show();

                }
            });
        }

        removeStateSearch_M = function () {
            $("#lblStateCode").text('0');
            $("#lblStateName").text('');
            $("#lblDistrictCode").text('0');
            $("#lblDistrictName").text('');
            $('#myInput_M').val('');

            var StCode = $("#lblStateCode").text();
            var StName = $("#lblStateName").text();
            var tr_Search = '';
            var obj = {};
            obj.StCode = encodeTxt(StCode);
            obj.Name = encodeTxt('');
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/JJM_StateDistrictSearch',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {
                    if (StCode == '0' || StCode == '') {
                        //$("#myInput").attr("placeholder", "Search state ...");
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your state</b><i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="closetable()"></i></th>';
                        tr_Search += ' </tr> </thead>';
                    }
                    else {
                        //$("#myInput").attr("placeholder", "Search district ...");
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + StName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="removeStateSearch_M()"></i></div></th><tr>';
                        tr_Search += '<tr><th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your district</b></th>';
                        tr_Search += ' </tr> </thead>';
                    }

                    tr_Search += '<tbody><tr><td>';
                    for (var i = 0; i < data.d.length; i++) {
                        if (StCode == '0' || StCode == '') {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataStateClick_M(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';

                        }
                        else {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataDistrictClick_M(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        tr_Search += '' + toTitleCase(data.d[i].KeyName) + '</div>';
                    }
                    tr_Search += '</td></tr></tbody>';
                    $("#tbl_search_M").html("");
                    $("#tbl_search_M").append(tr_Search);
                    $("#tbl_search_M").show();
                }
            });
        }

        //============Certified District,Block List------
        getdateCertifiedDistrictBlock = function (Id, Cer_Cat) {

            var val = $('#' + Id).text();
            if (val == "0") {
                return;
            }
            var obj = {};
            obj.StCode11 = encodeTxt(G_StCode);
            obj.DtCode11 = encodeTxt(G_DtCode);
            obj.Cer_Cat = encodeTxt(Cer_Cat);
            obj.Type = encodeTxt('0');
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/Bind_Certified_Details',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {
                    Bind_certified_District_Block(data, G_Cat, G_SubCat, G_Param, G_StCode, G_DtCode, Cer_Cat, '0', Lang);
                }
            });
        }

        //============After launch of mission data and State wise graph hide/show------
        display_missionReport = function () {
            var sign = $("#lblcollapse_expend").text();
            if (sign == '[+]') {
                $("#btn_download2").show();
                $("#div_mission").show().animate();
                $("#lblcollapse_expend").text("[-]");
            }
            else {
                $("#btn_download2").hide();
                $("#div_mission").hide().animate();
                $("#lblcollapse_expend").text("[+]");
            }
        }
        display_tapconngraph = function () {
            var sign = $("#lblcollapse_expend_graph").text();
            if (sign == '[+]') {
                $("#btn_downloadGraph").show();
                $("#div_graph").show().animate();
                $("#div_graph_type").show();
                $("#lblcollapse_expend_graph").text("[-]");
            }
            else {
                $("#btn_downloadGraph").hide();
                $("#div_graph").hide().animate();
                $("#div_graph_type").hide();
                $("#lblcollapse_expend_graph").text("[+]");
            }
        }
        display_financial = function () {
            var sign = $("#lblcollapse_expend_financial").text();
            if (sign == '[+]') {
                $("#financial_details").show();
                $("#financial_details").show().animate();
                $("#financial_tab").show();
                $("#lblcollapse_expend_financial").text("[-]");
            }
            else {
                $("#financial_details").hide();
                $("#financial_details").hide().animate();
                $("#financial_tab").hide();
                $("#lblcollapse_expend_financial").text("[+]");
            }
        }
        display_financial_M = function () {
            var sign = $("#lblcollapse_expend_financial_M").text();
            if (sign == '[+]') {
                $("#financial_details_M").show();
                $("#financial_details_M").show().animate();
                $("#financial_tab_M").show();
                $("#lblcollapse_expend_financial_M").text("[-]");
            }
            else {
                $("#financial_details_M").hide();
                $("#financial_details_M").hide().animate();
                $("#financial_tab_M").hide();
                $("#lblcollapse_expend_financial_M").text("[+]");
            }
        }

        display_HGJ = function () {
            var sign = $("#lblcollapse_expend_HGJ").text();
            if (sign == '[+]') {
                $("#div_HGJ_export").show();
                $("#div_tbl_HGJ").show().animate();
                $("#lblcollapse_expend_HGJ").text("[-]");
            }
            else {
                $("#div_HGJ_export").hide();
                $("#div_tbl_HGJ").hide().animate();
                $("#lblcollapse_expend_HGJ").text("[+]");
            }
        }

        open_hargharjal_info = function (type) {
            if (type == 0) {
                $("#div_harghar_jal_about").show();
                $("#div_harghar_jal_reported").hide();
                $("#div_harghar_jal_certified").hide();
                $("#HGJ_info_PopHead").html('');
                $("#HGJ_info_PopHead").html('About Har Ghar Jal');
            }
            else if (type == 1) {
                $("#div_harghar_jal_about").hide();
                $("#div_harghar_jal_reported").show();
                $("#div_harghar_jal_certified").hide();
                $("#HGJ_info_PopHead").html('');
                $("#HGJ_info_PopHead").html("About 'Reported' Har Ghar Jal");
            }
            else if (type == 2) {
                $("#div_harghar_jal_about").hide();
                $("#div_harghar_jal_reported").hide();
                $("#div_harghar_jal_certified").show();
                $("#HGJ_info_PopHead").html('');
                $("#HGJ_info_PopHead").html("About 'Certified' Har Ghar Jal");
            }
            document.getElementById('ModelHGJ_info_Pop_Id').style.display = "block";

        }

    });
};
function getCurrentDate() {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1; //January is 0!

    var yyyy = today.getFullYear();
    if (dd < 10) {
        dd = '0' + dd;
    }
    if (mm < 10) {
        mm = '0' + mm;
    }
    var today = dd + '/' + mm + '/' + yyyy;
    return today;
}
function toTitleCase(str) {
    if (str == 'D&NH and D&D') {
        return str;
    }
    else {
        return str.replace(/\w\S*/g, function (txt) { return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase(); });
    }
}
var encN = 1;
function encodeTxt(s) {
    //console.log(encN);
    s = escape(s);
    var ta = new Array();
    for (i = 0; i < s.length; i++) ta[i] = s.charCodeAt(i) + encN;
    return "" + escape(eval("String.fromCharCode(" + ta + ")")) + encN;
}
function getColorTable(cat, subcat, param, legendIdx, stcode) {
    try {
        var themeId = localStorage.getItem("themeId")
        if (typeof (themeId) == "undefined" || themeId == null) {
            themeId = 0;
        }
        if (stcode == "0") {
            if (themeId == 0) {
                return legends_S['Cat' + cat]['SubCat' + subcat]['Param' + param][legendIdx]['color'];
            }
            else {
                return legends_S['Cat' + cat]['SubCat' + subcat]['Param' + param][legendIdx]['color' + themeId];
            }
        }
        else {
            if (themeId == 0) {
                return legends_D['Cat' + cat]['SubCat' + subcat]['Param' + param][legendIdx]['color'];
            }
            else {
                return legends_D['Cat' + cat]['SubCat' + subcat]['Param' + param][legendIdx]['color' + themeId];
            }

        }

    } catch (e) {
        return 'rgba(255,255,255,0)';
    }
}
function getColorToday(cat, subcat, param, legendIdx, stcode) {
    try {
        var themeId = localStorage.getItem("themeId")
        if (typeof (themeId) == "undefined" || themeId == null) {
            themeId = 0;
        }
        if (stcode == "0") {
            if (themeId == 0) {
                return legends_S['Cat' + cat]['SubCat' + subcat]['Param' + param][legendIdx]['colorToday'];
            }
            else {
                return legends_S['Cat' + cat]['SubCat' + subcat]['Param' + param][legendIdx]['colorToday'];
            }
        }
        else {
            if (themeId == 0) {
                return legends_D['Cat' + cat]['SubCat' + subcat]['Param' + param][legendIdx]['colorToday'];
            }
            else {
                return legends_D['Cat' + cat]['SubCat' + subcat]['Param' + param][legendIdx]['colorToday'];
            }

        }

    } catch (e) {
        return 'rgba(255,255,255,0)';
    }
}
function getForeColorTable(cat, subcat, param, legendIdx, stcode) {
    try {
        var themeId = localStorage.getItem("themeId")
        if (typeof (themeId) == "undefined" || themeId == null) {
            themeId = 0;
        }
        if (stcode == "0") {
            return legends_S['Cat' + cat]['SubCat' + subcat]['Param' + param][legendIdx]['colorTableFont'];
        }
        else {
            return legends_D['Cat' + cat]['SubCat' + subcat]['Param' + param][legendIdx]['colorTableFont'];
        }

    } catch (e) {
        return 'rgba(255,255,255,0)';
    }
}

function sortByKeyAsc(array, key, IsNumeric) {
    return array.sort(function (a, b) {
        var x;
        var y;
        if (IsNumeric == true) {
            x = parseFloat(a[key]);
            y = parseFloat(b[key]);
        }
        else {
            x = a[key];
            y = b[key];
        }
        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
    });
}
function sortByKeyDsc(array, key, IsNumeric) {
    return array.sort(function (a, b) {
        var x;
        var y;
        if (IsNumeric == true) {
            x = parseFloat(a[key]);
            y = parseFloat(b[key]);
        }
        else {
            x = a[key];
            y = b[key];
        }
        return ((x > y) ? -1 : ((x < y) ? 1 : 0));
    });
}
function Fhtc_info(data, G_Cat, G_SubCat, G_Param, G_StCode) {
    stArr_D = [];
    stArr_B = [];
    stArr_P = [];
    stArr_V = [];
    DataArr_D = [];
    DataArr_B = [];
    DataArr_P = [];
    DataArr_V = [];


    var NoofDistrictHGJ_Today_Total = 0;
    var NoofBlockHGJ_Today_Total = 0;
    var NoofPanchayatHGJ_Today_Total = 0;
    var NoofvillageHGJ_Today_Total = 0;

    var NoofDistrictHGJCertified_Today_Total = 0;
    var NoofBlockHGJCertified_Today_Total = 0;
    var NoofPanchayatHGJCertified_Today_Total = 0;
    var NoofvillageHGJCertified_Today_Total = 0;


    var State_Coverage_Total = 0;
    var District_Coverage_Total = 0;
    var Block_Coverage_Total = 0;
    var Panchayat_Coverage_Total = 0;
    var Village_Coverage_Total = 0.00;
    var Habitation_Coverage_Total = 0;

    var District_Certified_Total = 0;
    var Block_Certified_Total = 0;
    var Panchayat_Certified_Total = 0;
    var Village_Certified_Total = 0;

    var Village_Total = 0;

    var grapharray = data.d;

    grapharray = sortByKeyAsc(data.d, "Name", false);

    var tr = "";
    for (var i = 0; i < grapharray.length; i++) {
        tr += '<tr class="item">';
        if (Lang == 'hi') {
            tr += '<td class="jjm-left-align jjm-tableleftpadding "><div class="jjm-col l12 m12 s12"><a href="javascript:getStateClick(' + "'" + G_Cat + "'" + ',' + "'" + G_SubCat + "'" + ',' + "'" + G_Param + "'" + ',' + "'" + grapharray[i].KeyValue + "'" + ',' + "'" + toTitleCase(grapharray[i].Name_hi) + "'" + ')" style="text-decoration: none;">' + toTitleCase(grapharray[i].Name_hi) + '</a></div></td>';
        }
        else {
            tr += '<td class="jjm-left-align jjm-tableleftpadding "><div class="jjm-col l12 m12 s12"><a href="javascript:getStateClick(' + "'" + G_Cat + "'" + ',' + "'" + G_SubCat + "'" + ',' + "'" + G_Param + "'" + ',' + "'" + grapharray[i].KeyValue + "'" + ',' + "'" + toTitleCase(grapharray[i].Name) + "'" + ')" style="text-decoration: none;">' + toTitleCase(grapharray[i].Name) + '</a></div></td>';
        }

        //tr += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">' + numberWithCommas(grapharray[i].NoofVillage, 0, 0) + '</div></td>';
        tr += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">' + numberWithCommas(grapharray[i].Village_Coverage, 0, 0) + '</div></td>';
        tr += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">' + numberWithCommas(grapharray[i].Village_Certified, 0, 0) + '</div></td>';
        var Village_Certified_Per = 0.00;
        if (parseFloat(grapharray[i].Village_Coverage) == 0) {
            Village_Certified_Per = 0.00;
        }
        else {
            Village_Certified_Per = (parseFloat(grapharray[i].Village_Certified) * 100.00) / parseFloat(grapharray[i].Village_Coverage);
        }
        tr += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">' + Village_Certified_Per.toFixed(2) + '</div></td>';

        /************************Begin Sort****************************/
        tr += '<td class="jjm-hide">' + grapharray[i].Village_Coverage + '</td>';
        tr += '<td class="jjm-hide">' + grapharray[i].Village_Certified + '</td>';

        /**********************End Sort******************************/

        tr += '</tr>';
    }


    grapharray = sortByKeyAsc(grapharray, "District_Coverage", true);
    for (var i = 0; i < grapharray.length; i++) {
        if (parseFloat(grapharray[i].District_Coverage) != 0) {
            stArr_D.push(toTitleCase(grapharray[i].Name));
            DataArr_D.push(parseFloat(grapharray[i].District_Coverage));
        }
        State_Coverage_Total += parseFloat(grapharray[i].State_Coverage);
        District_Coverage_Total += parseFloat(grapharray[i].District_Coverage);
        Block_Coverage_Total += parseFloat(grapharray[i].Block_Coverage);
        Panchayat_Coverage_Total += parseFloat(grapharray[i].Panchayat_Coverage);
        Village_Coverage_Total += parseFloat(grapharray[i].Village_Coverage);
        Habitation_Coverage_Total += parseFloat(grapharray[i].Habitation_Coverage);
        Village_Total += parseFloat(grapharray[i].NoofVillage);

        District_Certified_Total += parseFloat(grapharray[i].District_Certified);
        Block_Certified_Total += parseFloat(grapharray[i].Block_Certified);
        Panchayat_Certified_Total += parseFloat(grapharray[i].Panchayat_Certified);
        Village_Certified_Total += parseFloat(grapharray[i].Village_Certified);

        NoofDistrictHGJ_Today_Total += parseFloat(grapharray[i].NoofDistrictHGJ_Today);
        NoofBlockHGJ_Today_Total += parseFloat(grapharray[i].NoofBlockHGJ_Today);
        NoofPanchayatHGJ_Today_Total += parseFloat(grapharray[i].NoofPanchayatHGJ_Today);
        NoofvillageHGJ_Today_Total += parseFloat(grapharray[i].NoofvillageHGJ_Today);

        NoofDistrictHGJCertified_Today_Total += parseFloat(grapharray[i].NoofDistrictHGJCertified_Today);
        NoofBlockHGJCertified_Today_Total += parseFloat(grapharray[i].NoofBlockHGJCertified_Today);
        NoofPanchayatHGJCertified_Today_Total += parseFloat(grapharray[i].NoofPanchayatHGJCertified_Today);
        NoofvillageHGJCertified_Today_Total += parseFloat(grapharray[i].NoofvillageHGJCertified_Today);
    }
    grapharray = sortByKeyAsc(grapharray, "Block_Coverage", true);
    for (var i = 0; i < grapharray.length; i++) {
        if (parseFloat(grapharray[i].Block_Coverage) != 0) {
            stArr_B.push(toTitleCase(grapharray[i].Name));
            DataArr_B.push(parseFloat(grapharray[i].Block_Coverage));
        }
    }
    grapharray = sortByKeyAsc(grapharray, "Panchayat_Coverage", true);
    for (var i = 0; i < grapharray.length; i++) {
        if (parseFloat(grapharray[i].Panchayat_Coverage) != 0) {
            stArr_P.push(toTitleCase(grapharray[i].Name));
            DataArr_P.push(parseFloat(grapharray[i].Panchayat_Coverage));
        }
    }
    grapharray = sortByKeyAsc(grapharray, "Village_Coverage", true);
    for (var i = 0; i < grapharray.length; i++) {
        if (parseFloat(grapharray[i].Village_Coverage) != 0) {
            stArr_V.push(toTitleCase(grapharray[i].Name));
            DataArr_V.push(parseFloat(grapharray[i].Village_Coverage));
        }
    }
    grapharray = sortByKeyAsc(grapharray, "Orderby", true);
    var str100PerState = '';
    var strCertifiedState = '';
    var count100Per = 0;
    for (var i = 0; i < grapharray.length; i++) {
        if (parseFloat(grapharray[i].State_Coverage) != 0 && parseFloat(grapharray[i].State_Certified) == 0) {
            if (str100PerState == '') {
                if (Lang == 'hi') {
                    str100PerState += toTitleCase(grapharray[i].Name_hi);
                }
                else {
                    str100PerState += toTitleCase(grapharray[i].Name);
                }
            }
            else {
                if (Lang == 'hi') {
                    str100PerState += ', ' + toTitleCase(grapharray[i].Name_hi);
                }
                else {
                    str100PerState += ', ' + toTitleCase(grapharray[i].Name);
                }

            }
        }
        if (parseFloat(grapharray[i].State_Certified) != 0) {
            if (strCertifiedState == '') {
                if (Lang == 'hi') {
                    strCertifiedState += toTitleCase(grapharray[i].Name_hi);
                }
                else {
                    strCertifiedState += toTitleCase(grapharray[i].Name);
                }
            }
            else {
                if (Lang == 'hi') {
                    strCertifiedState += ', ' + toTitleCase(grapharray[i].Name_hi);
                }
                else {
                    strCertifiedState += ', ' + toTitleCase(grapharray[i].Name);
                }

            }
        }
    }
    $("#lblHCState").html(str100PerState);
    $("#lblHCState_M").html(str100PerState);
    if (strCertifiedState == "") {
        strCertifiedState = "--";
    }
    $("#lblHCState_C").html(strCertifiedState);
    $("#lblHCState_C_M").html(strCertifiedState);

    startRunning();
    startRunning_M();

    $('#lblHCDistrict').text(numberWithCommas(District_Coverage_Total, 0, 0));
    $('#lblHCBlock').text(numberWithCommas(Block_Coverage_Total, 0, 0));
    $('#lblHCPanchayat').text(numberWithCommas(Panchayat_Coverage_Total, 0, 0));
    $('#lblHCVillage').text(numberWithCommas(Village_Coverage_Total, 0, 0));


    if (parseInt(NoofDistrictHGJ_Today_Total) == 0) {
        $('#hide_DistrictHGJ').hide();
        $('#hide_DistrictHGJ_M').hide();
    } else {
        $('#hide_DistrictHGJ').show();
        $('#hide_DistrictHGJ_M').show();
        $('#lblNoofDistrictHGJ_Today').text(numberWithCommas(NoofDistrictHGJ_Today_Total, 0, 0));
        $('#lblNoofDistrictHGJ_Today_M').text(numberWithCommas(NoofDistrictHGJ_Today_Total, 0, 0));
    }
    if (parseInt(NoofBlockHGJ_Today_Total) == 0) {
        $('#hide_BlockHGJ').hide();
        $('#hide_BlockHGJ_M').hide();
    } else {
        $('#hide_BlockHGJ').show();
        $('#hide_BlockHGJ_M').show();
        $('#lblNoofBlockHGJ_Today').text(numberWithCommas(NoofBlockHGJ_Today_Total, 0, 0));
        $('#lblNoofBlockHGJ_Today_M').text(numberWithCommas(NoofBlockHGJ_Today_Total, 0, 0));
    }
    if (parseInt(NoofPanchayatHGJ_Today_Total) == 0) {
        $('#hide_PanchayatHGJ').hide();
        $('#hide_PanchayatHGJ_M').hide();
    } else {
        $('#hide_PanchayatHGJ').show();
        $('#hide_PanchayatHGJ_M').show();
        $('#lblNoofPanchayatHGJ_Today').text(numberWithCommas(NoofPanchayatHGJ_Today_Total, 0, 0));
        $('#lblNoofPanchayatHGJ_Today_M').text(numberWithCommas(NoofPanchayatHGJ_Today_Total, 0, 0));
    }
    if (parseInt(NoofvillageHGJ_Today_Total) == 0) {
        $('#hide_VillageHGJ').hide();
        $('#hide_VillageHGJ_M').hide();
    } else {
        $('#hide_VillageHGJ').show();
        $('#hide_VillageHGJ_M').show();
        $('#lblNoofvillageHGJ_Today').text(numberWithCommas(NoofvillageHGJ_Today_Total, 0, 0));
        $('#lblNoofvillageHGJ_Today_M').text(numberWithCommas(NoofvillageHGJ_Today_Total, 0, 0));
    }


    //$("#lblHCState").text(State_Coverage_Total);
    $('#lblHCDistrict_M').text(numberWithCommas(District_Coverage_Total, 0, 0));
    $('#lblHCBlock_M').text(numberWithCommas(Block_Coverage_Total, 0, 0));
    $('#lblHCPanchayat_M').text(numberWithCommas(Panchayat_Coverage_Total, 0, 0));
    $('#lblHCVillage_M').text(numberWithCommas(Village_Coverage_Total, 0, 0));

    $('#lblHCDistrict_C').text(numberWithCommas(District_Certified_Total, 0, 0));
    $('#lblHCBlock_C').text(numberWithCommas(Block_Certified_Total, 0, 0));
    $('#lblHCPanchayat_C').text(numberWithCommas(Panchayat_Certified_Total, 0, 0));
    $('#lblHCVillage_C').text(numberWithCommas(Village_Certified_Total, 0, 0));

    $('#lblHCDistrict_C_M').text(numberWithCommas(District_Certified_Total, 0, 0));
    $('#lblHCBlock_C_M').text(numberWithCommas(Block_Certified_Total, 0, 0));
    $('#lblHCPanchayat_C_M').text(numberWithCommas(Panchayat_Certified_Total, 0, 0));
    $('#lblHCVillage_C_M').text(numberWithCommas(Village_Certified_Total, 0, 0));


    //==========Certified HGJ today========
    if (parseInt(NoofDistrictHGJCertified_Today_Total) == 0) {
        $('#hide_DistrictHGJCertified').hide();
        $('#hide_DistrictHGJCertified_M').hide();
    } else {
        $('#hide_DistrictHGJCertified').show();
        $('#hide_DistrictHGJCertified_M').show();
        $('#lblNoofDistrictHGJCertified_Today').text(numberWithCommas(NoofDistrictHGJCertified_Today_Total, 0, 0));
        $('#lblNoofDistrictHGJCertified_Today_M').text(numberWithCommas(NoofDistrictHGJCertified_Today_Total, 0, 0));
    }
    if (parseInt(NoofBlockHGJCertified_Today_Total) == 0) {
        $('#hide_BlockHGJCertified').hide();
        $('#hide_BlockHGJCertified_M').hide();
    } else {
        $('#hide_BlockHGJCertified').show();
        $('#hide_BlockHGJCertified_M').show();
        $('#lblNoofBlockHGJCertified_Today').text(numberWithCommas(NoofBlockHGJCertified_Today_Total, 0, 0));
        $('#lblNoofBlockHGJCertified_Today_M').text(numberWithCommas(NoofBlockHGJCertified_Today_Total, 0, 0));
    }
    if (parseInt(NoofPanchayatHGJCertified_Today_Total) == 0) {
        $('#hide_PanchayatHGJCertified').hide();
        $('#hide_PanchayatHGJCertified_M').hide();
    } else {
        $('#hide_PanchayatHGJCertified').show();
        $('#hide_PanchayatHGJCertified_M').show();
        $('#lblNoofPanchayatHGJCertified_Today').text(numberWithCommas(NoofPanchayatHGJCertified_Today_Total, 0, 0));
        $('#lblNoofPanchayatHGJCertified_Today_M').text(numberWithCommas(NoofPanchayatHGJCertified_Today_Total, 0, 0));
    }
    if (parseInt(NoofvillageHGJCertified_Today_Total) == 0) {
        $('#hide_VillageHGJCertified').hide();
        $('#hide_VillageHGJCertified_M').hide();
    } else {
        $('#hide_VillageHGJCertified').show();
        $('#hide_VillageHGJCertified_M').show();
        $('#lblNoofvillageHGJCertified_Today').text(numberWithCommas(NoofvillageHGJCertified_Today_Total, 0, 0));
        $('#lblNoofvillageHGJCertified_Today_M').text(numberWithCommas(NoofvillageHGJCertified_Today_Total, 0, 0));
    }


    var tr_foot = '';
    tr_foot += '<tr style="font-weight:600;" class="jjm-light-gray">';
    tr_foot += '<td class="jjm-left-align jjm-tableleftpadding "><div class="jjm-col l12 m12 s12">Total</div></td>';
    //tr_foot += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">' + numberWithCommas(Village_Total, 0, 0) + '</div></td>';
    tr_foot += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">' + numberWithCommas(Village_Coverage_Total, 0, 0) + '</div></td>';
    tr_foot += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">' + numberWithCommas(Village_Certified_Total, 0, 0) + '</div></td>';
    tr_foot += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">' + parseFloat(Village_Certified_Total * 100 / Village_Coverage_Total).toFixed(2) + '</div></td>';
    tr_foot += '</tr>';
    $("#tblBody_HGJ").empty();
    $("#tblFoot_HGJ").empty();

    $("#tblBody_HGJ").append(tr);
    $("#tblFoot_HGJ").append(tr_foot);

    FHTC_Chart_info(stArr_D, DataArr_D, "FHTC_Chart_District", '#EBF1FB', 'Districts', Lang);
    FHTC_Chart_info(stArr_B, DataArr_B, "FHTC_Chart_Block", '#ffdddd', 'Blocks', Lang);
    FHTC_Chart_info(stArr_P, DataArr_P, "FHTC_Chart_Panchayat", '#ffffcc', 'Panchayts', Lang);
    FHTC_Chart_info(stArr_V, DataArr_V, "FHTC_Chart_Village", '#ddffdd', 'Villages', Lang);

    $("#FHTC_Chart_District").hide();
    $("#FHTC_Chart_Block").hide();
    $("#FHTC_Chart_Panchayat").hide();
    $("#FHTC_Chart_Village").hide();
}
function StateWiseFHTCTap(data, G_Cat, G_SubCat, G_Param, G_StCode, value, Lang) {

    var titlecontent = "";
    titlecontent = "State Wise Household tap connection provided";

    var HouseholdAsondate_Total = 0;
    var HouseholdTapConAsondate_Total = 0;
    var HouseholdTapConToday_Total = 0;
    var HouseholdTapConPer = 0.00;

    var year01042019_Total = 0;
    var remain_HH_year01042019_Total = 0;

    stateArr = [];
    baseline010419_Arr = [];
    baseline010420_Arr = [];
    current20_21_Arr = [];
    remainArr = [];
    achiveArr = [];

    remain_15082019_Arr = [];
    achive_15082019_Arr = [];
    Mission_Arr = [];
    achive_M_Arr = [];
    $("#tblBody").empty();
    var tr = "";
    var tr_Search = '';

    $("#tblBody2").empty();
    var tr_Mission = "";

    $("#tblBody3").empty();
    var tr_Mission_baseline = "";

    for (var i = 0; i < data.d.length; i++) {
        var colorId = data.d[i].ColorId;
        tr += '<tr class="item" style="background-color:' + getColorTable(G_Cat, G_SubCat, G_Param, colorId, G_StCode) + ';color:' + getForeColorTable(G_Cat, G_SubCat, G_Param, colorId, G_StCode) + ';">';
        if (Lang == 'hi') {
            tr += '<td class="jjm-left-align jjm-tableleftpadding "><div class="jjm-col l12 m12 s12">&nbsp;</div><div class="jjm-col l12 m12 s12"><a href="javascript:getStateClick(' + "'" + G_Cat + "'" + ',' + "'" + G_SubCat + "'" + ',' + "'" + G_Param + "'" + ',' + "'" + data.d[i].KeyValue + "'" + ',' + "'" + toTitleCase(data.d[i].Name_hi) + "'" + ')" style="text-decoration: none;">' + toTitleCase(data.d[i].Name_hi) + '</a></div></td>';
        }
        else {
            tr += '<td class="jjm-left-align jjm-tableleftpadding "><div class="jjm-col l12 m12 s12">&nbsp;</div><div class="jjm-col l12 m12 s12"><a href="javascript:getStateClick(' + "'" + G_Cat + "'" + ',' + "'" + G_SubCat + "'" + ',' + "'" + G_Param + "'" + ',' + "'" + data.d[i].KeyValue + "'" + ',' + "'" + toTitleCase(data.d[i].Name) + "'" + ')" style="text-decoration: none;">' + toTitleCase(data.d[i].Name) + '</a></div></td>';
        }
        //tr += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">&nbsp;</div><div class="jjm-col l12 m12 s12">' + numberWithCommas(data.d[i].Total, 0, 0) + '</div></td>';
        tr += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">&nbsp;</div><div class="jjm-col l12 m12 s12">' + numberWithCommas(data.d[i].Total, 0, 0) + '</div></td>';

        //tr += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">' + numberWithCommas(data.d[i].Value, 0, 0) + '</div></td>';
        if (parseFloat(data.d[i].Today) == 0) {
            if (parseFloat(data.d[i].Total) == parseFloat(data.d[i].Value)) {
                tr += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">&nbsp;</div><div class="jjm-col l12 m12 s12">' + numberWithCommas(data.d[i].Value, 0, 0) + '</div></td>';
            }
            else {
                tr += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12 jjm-right-align" style="color:' + getColorToday(G_Cat, G_SubCat, G_Param, colorId, G_StCode) + '"><b>' + data.d[i].Today + '</b></div><div class="jjm-col l12 m12 s12">' + numberWithCommas(data.d[i].Value, 0, 0) + '</div></td>';
            }
        }
        else {
            tr += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12 jjm-right-align" style="color:' + getColorToday(G_Cat, G_SubCat, G_Param, colorId, G_StCode) + '"><b>+ ' + data.d[i].Today + '</b></div><div class="jjm-col l12 m12 s12">' + numberWithCommas(data.d[i].Value, 0, 0) + '</div></td>';
        }
        tr += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">&nbsp;</div><div class="jjm-col l12 m12 s12">' + data.d[i].Per + '</div></td>';

        /************************Begin Sort****************************/
        tr += '<td class="jjm-hide">' + data.d[i].Total + '</td>';
        tr += '<td class="jjm-hide">' + data.d[i].Value + '</td>';

        /**********************End Sort******************************/

        tr += '</tr>';


        var colorId2 = 0;
        var Value_JJMMission = parseFloat(parseFloat(data.d[i].Value) - parseFloat(data.d[i].HCPWS_01042019));

        if (Value_JJMMission <= 0) {
            Value_JJMMission = 0;
        }
        var remain_HH_year01042019 = 0;
        remain_HH_year01042019 = parseFloat(data.d[i].Total) - parseFloat(data.d[i].HCPWS_01042019);
        if (remain_HH_year01042019 <= 0) {
            remain_HH_year01042019 = 0;
        }


        var Per_JJMMission = 0.00;
        if (data.d[i].Total == "0") {
            Per_JJMMission = 0.00;
            colorId2 = 0;
        }
        else {
            if (remain_HH_year01042019 <= 0 || Value_JJMMission <= 0) {
                Per_JJMMission = 0.00;
                colorId2 = 0;
            }
            else {
                Per_JJMMission = parseFloat(parseFloat(parseFloat(Value_JJMMission * 100.00) / parseFloat(remain_HH_year01042019)).toFixed(2));
            }
            if (Per_JJMMission >= 0 & Per_JJMMission <= 10.00) {
                colorId2 = 0;
            }
            else if (Per_JJMMission > 10 & Per_JJMMission <= 25.00) {
                colorId2 = 1;
            }
            else if (Per_JJMMission > 25 & Per_JJMMission <= 50.00) {
                colorId2 = 2;
            }
            else if (Per_JJMMission > 50 & Per_JJMMission <= 75.00) {
                colorId2 = 3;
            }
            else if (Per_JJMMission > 75 & Per_JJMMission < 100.00) {
                colorId2 = 4;
            }
            else {
                colorId2 = 5;
            }
        }
        Mission_Arr.push({
            "colorId": colorId2,
            "Name": toTitleCase(data.d[i].Name),
            "Name_hi": data.d[i].Name_hi,
            "Per": Per_JJMMission.toFixed(2),
            "Value": Value_JJMMission,
            "Total": remain_HH_year01042019
        }
        )

        tr_Search += '<tr>';
        tr_Search += '<td class="jjm-left-align" style="padding-left:35px;width:100%;"><a href="javascript:getdataStateClick(' + "'" + G_Cat + "'" + ',' + "'" + G_SubCat + "'" + ',' + "'" + G_Param + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + data.d[i].Name + "'" + ')" style="text-decoration:none; text-decoration-line:none;"><i class="fa fa-tint jjm-margin-right jjm-text-light-blue" aria-hidden="true"></i>' + data.d[i].Name + '</a></td>';
        tr_Search += '</tr>';

        HouseholdAsondate_Total += parseFloat(data.d[i].Total);
        HouseholdTapConAsondate_Total += parseFloat(data.d[i].Value);
        HouseholdTapConToday_Total += parseFloat(data.d[i].Today);

        year01042019_Total += parseFloat(data.d[i].HCPWS_01042019);


    }

    Mission_Arr = sortByKeyDsc(Mission_Arr, "Per", true);
    var HouseholdTapCon_Mission_Total = 0;
    for (var i = 0; i < Mission_Arr.length; i++) {
        tr_Mission += '<tr class="item">';
        if (Lang == 'hi') {
            tr_Mission += '<td class="jjm-left-align jjm-tableleftpadding "><div class="jjm-col l12 m12 s12">' + Mission_Arr[i].Name_hi + '</div></td>';
        }
        else {
            tr_Mission += '<td class="jjm-left-align jjm-tableleftpadding "><div class="jjm-col l12 m12 s12">' + toTitleCase(Mission_Arr[i].Name) + '</div></td>';
        }
        tr_Mission += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">' + numberWithCommas(Mission_Arr[i].Total, 0, 0) + '</div></td>';
        tr_Mission += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">' + numberWithCommas(Mission_Arr[i].Value, 0, 0) + '</div></td>';
        tr_Mission += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">' + Mission_Arr[i].Per + '</div></td>';

        /************************Begin Sort****************************/
        tr_Mission += '<td class="jjm-hide">' + Mission_Arr[i].Total + '</td>';
        tr_Mission += '<td class="jjm-hide">' + Mission_Arr[i].Value + '</td>';

        /**********************End Sort******************************/

        tr_Mission += '</tr>';
        HouseholdTapCon_Mission_Total += parseFloat(Mission_Arr[i].Value);
        remain_HH_year01042019_Total += parseFloat(Mission_Arr[i].Total);
    }

    var grapharray = data.d;
    grapharray = sortByKeyAsc(grapharray, "Per_HC_Remain", true);
    for (var i = 0; i < grapharray.length; i++) {
        if (Lang == 'hi') {
            stateArr.push(grapharray[i].Name_hi);
        }
        else {
            stateArr.push(toTitleCase(grapharray[i].Name));
        }
        baseline010419_Arr.push(parseFloat(grapharray[i].Per_HCPWS_01042019));
        baseline010420_Arr.push(parseFloat(grapharray[i].Per_HCPWS_19_20));
        current20_21_Arr.push(parseFloat(grapharray[i].Per_HCPWS_20_21));

        remainArr.push(parseFloat(grapharray[i].HC_Remain));
        var colorId = data.d[i].ColorId;
        achiveArr.push(
            { y: parseFloat(grapharray[i].Value), color: getColorTable(G_Cat, G_SubCat, G_Param, colorId, G_StCode) }//
        )
        achive_M_Arr.push(
            {
                y: parseFloat(grapharray[i].HCPWS_20_21), color: 'rgba(189, 215, 231, 1)'
            }
        )
        var remain_15082019 = parseFloat(grapharray[i].Total) - parseFloat(data.d[i].HCPWS_01042019);

        remain_15082019_Arr.push(parseFloat(remain_15082019));
        achive_15082019_Arr.push(
            { y: parseFloat(grapharray[i].HCPWS_01042019), color: getColorTable(G_Cat, G_SubCat, G_Param, colorId, G_StCode) }//
        )
    }

    var table_Header_desc;
    if (Lang == 'en') {
        table_Header_desc = Table_HeaderDesc['Cat' + G_Cat]['SubCat' + G_SubCat]['Param' + G_Param];
    }
    else {
        table_Header_desc = Table_HeaderDesc_hi['Cat' + G_Cat]['SubCat' + G_SubCat]['Param' + G_Param];
    }

    var tr_foot = '';
    tr_foot += '<tr style="font-weight:600;" class="jjm-light-gray">';
    tr_foot += '<td class="jjm-left-align jjm-tableleftpadding "><div class="jjm-col l12 m12 s12">&nbsp;</div><div class="jjm-col l12 m12 s12">' + table_Header_desc[0].desc_foot_total + '</div></td>';
    tr_foot += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">&nbsp;</div><div class="jjm-col l12 m12 s12">' + numberWithCommas(HouseholdAsondate_Total, 0, 0) + '</div></td>';
    tr_foot += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12 jjm-right-align" style="color:' + getColorToday(G_Cat, G_SubCat, G_Param, 1, 0) + '"><b>' + numberWithCommas(HouseholdTapConToday_Total, 0, 0) + '</b></div><div class="jjm-col l12 m12 s12">' + numberWithCommas(HouseholdTapConAsondate_Total, 0, 0) + '</div></td>';
    tr_foot += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">&nbsp;</div><div class="jjm-col l12 m12 s12">' + parseFloat(HouseholdTapConAsondate_Total * 100 / HouseholdAsondate_Total).toFixed(2) + '</div></td>';
    tr_foot += '</tr>';

    var tr_Mission_foot = '';
    tr_Mission_foot += '<tr style="font-weight:600;" class="jjm-light-gray">';
    tr_Mission_foot += '<td class="jjm-left-align jjm-tableleftpadding "><div class="jjm-col l12 m12 s12">' + table_Header_desc[0].desc_foot_total + '</div></td>';
    tr_Mission_foot += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">' + numberWithCommas(remain_HH_year01042019_Total, 0, 0) + '</div></td>';
    tr_Mission_foot += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">' + numberWithCommas(HouseholdTapCon_Mission_Total, 0, 0) + '</div></td>';
    tr_Mission_foot += '<td class="jjm-right-align"><div class="jjm-col l12 m12 s12">' + parseFloat(HouseholdTapCon_Mission_Total * 100 / remain_HH_year01042019_Total).toFixed(2) + '</div></td>';
    tr_Mission_foot += '</tr>';

    $("#tblBody").html("");
    $("#tblBody").append(tr);
    $("#tblFoot").html("");
    $("#tblFoot").append(tr_foot);

    $("#tblBody2").html("");
    $("#tblBody2").append(tr_Mission);

    $("#tblFoot2").html("");
    $("#tblFoot2").append(tr_Mission_foot);

    $("#tbl_search").html("");
    $("#tbl_search").append(tr_Search);

    $("#tbl_search_M").html("");
    $("#tbl_search_M").append(tr_Search);


    $(".se-pre-con3").fadeOut();
    $("#imgLoading3").fadeOut();

    HouseholdTapConPer = parseFloat(HouseholdTapConAsondate_Total * 100 / HouseholdAsondate_Total).toFixed(2);
    $('#lblHH').text(numberWithCommas(HouseholdAsondate_Total, 0, 0));
    $('#lblHC').text(numberWithCommas(HouseholdTapConAsondate_Total, 0, 0));
    $('#lblHCToday').text(numberWithCommas(HouseholdTapConToday_Total, 0, 0));
    $('#lblHCPer').text(HouseholdTapConPer);
    $('#lblHC_15082019').text(numberWithCommas(year01042019_Total, 0, 0));
    var HouseholdTapCon_15082019_Per = parseFloat(year01042019_Total * 100 / HouseholdAsondate_Total).toFixed(2);
    $('#lblHC_15082019_Per').text(HouseholdTapCon_15082019_Per);

    $('#lblHH_M').text(numberWithCommas(HouseholdAsondate_Total, 0, 0));
    $('#lblHC_M').text(numberWithCommas(HouseholdTapConAsondate_Total, 0, 0));
    $('#lblHCToday_M').text(numberWithCommas(HouseholdTapConToday_Total, 0, 0));
    $('#lblHCPer_M').text(HouseholdTapConPer);
    $('#lblHC_15082019_M').text(numberWithCommas(year01042019_Total, 0, 0));
    $('#lblHC_15082019_Per_M').text(HouseholdTapCon_15082019_Per);
    var HouseholdTapCon_Mission_Per = 0.00;
    if (remain_HH_year01042019_Total == 0) {
        HouseholdTapCon_Mission_Per = 0.00;
    }
    else {
        HouseholdTapCon_Mission_Per = parseFloat((HouseholdTapConAsondate_Total - year01042019_Total) * 100 / remain_HH_year01042019_Total).toFixed(2);
    }
    $('#lblHH_launch').text(numberWithCommas(remain_HH_year01042019_Total, 0, 0));
    $('#lblHH_launch_M').text(numberWithCommas(remain_HH_year01042019_Total, 0, 0));

    $('#lblHC_launch').text(numberWithCommas((HouseholdTapConAsondate_Total - year01042019_Total), 0, 0));
    $('#lblHCPer_launch').text(HouseholdTapCon_Mission_Per);
    $('#lblHC_launch_M').text(numberWithCommas((HouseholdTapConAsondate_Total - year01042019_Total), 0, 0));
    $('#lblHCPer_launch_M').text(HouseholdTapCon_Mission_Per);

    $("#btn_download2").hide();
    $("#div_mission").hide();

    $("#div_graph").hide();
    $("#div_graph_type").hide();

    getfillDashboard_data(0);

    FHTC_Chart(stateArr, baseline010419_Arr, baseline010420_Arr, current20_21_Arr, achiveArr, remainArr, remain_15082019_Arr, achive_15082019_Arr, 0, Lang, achive_M_Arr);
};
function getCurrentFinancialYear() {
    var fiscalyear = "";
    var today = new Date();
    if ((today.getMonth() + 1) <= 3) {
        fiscalyear = (today.getFullYear() - 1) + "-" + today.getFullYear()
    } else {
        fiscalyear = today.getFullYear() + "-" + (today.getFullYear() + 1)
    }
    return fiscalyear
}
function drawchart(monthArrCum, dataArr, monthArr, dataArr_M, yearArr, dataArr_Y, value, Lang) {
    var backcolor = '#FFFFFF';
    var colorfont = '#000';
    var themeId = localStorage.getItem("themeId");
    if (typeof (themeId) == "undefined" || themeId == null) {
        themeId = 0;
    }
    if (themeId == 0) {
        backcolor = '#FFFFFF';
        colorfont = '#000';
    }
    else {
        backcolor = '#1e1e30';
        colorfont = '#f1f1f1';
    }
    var graph_HeaderDesc;
    if (Lang == 'hi') {
        graph_HeaderDesc = Graph_HeaderDesc_hi['Cat0']['SubCat0']['Param0'];
    }
    else {
        graph_HeaderDesc = Graph_HeaderDesc['Cat0']['SubCat0']['Param0'];
    }
    if (value == 0) {
        DataArr = dataArr;
        gType = 'area';
        $('#myChart').highcharts({
            chart: {
                //height: '70%',
                height: (9 / 16 * 100) + '%',
                type: gType,
                backgroundColor: backcolor,
                color: colorfont
            },
            title: {
                style: {
                    color: 'rgb(0, 0, 0)',
                    fontWeight: 'bold'
                },
                //x: titlePos,
                useHTML: true,
                text: '<div style="text-align:center;margin-right:100px;"></div>'
            },
            subtitle: {
                text: ''
            },
            exporting: {
                enabled: false
            },
            xAxis: {
                categories: monthArrCum,
                plotBands: [{ // visualize the weekend

                    color: 'rgba(68, 170, 213, .2)'
                }],
                labels: {
                    style: {
                        color: colorfont,
                        cursor: "default",
                        fontSize: "10px"
                    }
                },
                min: 0
            },
            yAxis: {
                tickPositioner: function () {

                    var positions = [],
                        //tick = Math.floor(this.dataMin),
                        tick = Math.floor(32000000),
                        increment = Math.abs(Math.ceil((Math.round(this.dataMax / 1000000) * 1000000 - tick) / 5));

                    if (this.dataMax !== null && this.dataMin !== null) {
                        for (tick; tick - increment <= this.dataMax; tick += increment) {
                            positions.push(tick);
                        }
                    }
                    return positions;
                },
                //tickInterval: 100000,
                title:
                {
                    text: graph_HeaderDesc[0].desc_Monthly,
                    style: {
                        color: colorfont,
                        fontSize: "9px"
                    }
                },
                gridLineWidth: 0,
                labels: {
                    style: {
                        color: colorfont,
                        cursor: "default",
                        fontSize: "10px"
                    },
                    formatter: function () {
                        return this.value / 100000 + " " + graph_HeaderDesc[0].desc_Rs;
                    }
                }
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                areaspline: {
                    fillOpacity: 0.5
                }
            },
            tooltip: {
                formatter: function () {
                    if (Lang == 'hi') {
                        return '' + this.series.name + ' ' + this.x + ' तक<br>: <b>' + numberWithCommas(this.y, 0, 0) + '</b>';
                    }
                    else {
                        return '' + this.series.name + ' upto ' + this.x + '<br>: <b>' + numberWithCommas(this.y, 0, 0) + '</b>';
                    }
                }
            },

            series: [{
                name: graph_HeaderDesc[0].desc_Monthly,
                data: DataArr,
                color: {
                    linearGradient: [0, 500, 500, 500],
                    stops: [
                        [0, 'rgba(234, 246, 255, .6)'],
                        [1, 'rgba(3, 158, 240, .8)']
                    ],
                    opacity: 0.3
                },
                lineColor: 'rgba(0, 121, 193, 1)',
            }
            ]
        });
        $('#myChart_M').highcharts({
            chart: {
                //height: '70%',
                height: (9 / 16 * 100) + '%',
                type: gType,
                backgroundColor: backcolor,
                color: colorfont
            },
            title: {
                style: {
                    color: 'rgb(0, 0, 0)',
                    fontWeight: 'bold'
                },
                //x: titlePos,
                useHTML: true,
                text: '<div style="text-align:center;margin-right:100px;"></div>'
            },
            subtitle: {
                text: ''
            },
            exporting: {
                enabled: false
            },
            xAxis: {
                categories: monthArrCum,
                plotBands: [{ // visualize the weekend

                    color: 'rgba(68, 170, 213, .2)'
                }],
                labels: {
                    style: {
                        color: colorfont,
                        cursor: "default",
                        fontSize: "10px"
                    }
                },
                min: 0
            },
            yAxis: {
                tickPositioner: function () {

                    var positions = [],
                        //tick = Math.floor(this.dataMin),
                        tick = Math.floor(32000000),
                        increment = Math.abs(Math.ceil((Math.round(this.dataMax / 1000000) * 1000000 - tick) / 5));

                    if (this.dataMax !== null && this.dataMin !== null) {
                        for (tick; tick - increment <= this.dataMax; tick += increment) {
                            positions.push(tick);
                        }
                    }
                    return positions;
                },
                //tickInterval: 100000,
                title:
                {
                    text: graph_HeaderDesc[0].desc_Monthly,
                    style: {
                        color: colorfont,
                        fontSize: "9px"
                    }
                },
                gridLineWidth: 0,
                labels: {
                    style: {
                        color: colorfont,
                        cursor: "default",
                        fontSize: "10px"
                    },
                    formatter: function () {
                        return this.value / 100000 + " " + graph_HeaderDesc[0].desc_Rs;
                    }
                }
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                areaspline: {
                    fillOpacity: 0.5
                }
            },
            tooltip: {
                formatter: function () {
                    if (Lang == 'hi') {
                        return '' + this.series.name + ' ' + this.x + ' तक<br>: <b>' + numberWithCommas(this.y, 0, 0) + '</b>';
                    }
                    else {
                        return '' + this.series.name + ' upto ' + this.x + '<br>: <b>' + numberWithCommas(this.y, 0, 0) + '</b>';
                    }
                }
            },

            series: [{
                name: graph_HeaderDesc[0].desc_Monthly,
                data: DataArr,
                color: {
                    linearGradient: [0, 500, 500, 500],
                    stops: [
                        [0, 'rgba(234, 246, 255, .6)'],
                        [1, 'rgba(3, 158, 240, .8)']
                    ],
                    opacity: 0.3
                },
                lineColor: 'rgba(0, 121, 193, 1)',
            }
            ]
        });
    }
    else if (value == 1) {
        DataArr = dataArr_M;
        gType = 'column';
        $('#myChart').highcharts({
            chart: {
                height: (9 / 16 * 100) + '%',
                //type: gType,
                backgroundColor: backcolor,
                color: colorfont
            },
            title: {
                style: {
                    color: 'rgb(0, 0, 0)',
                    fontWeight: 'bold'
                },
                //x: titlePos,
                useHTML: true,
                text: '<div style="text-align:center;margin-right:100px;"></div>'
            },
            subtitle: {
                text: ''
            },
            exporting: {
                enabled: false
            },
            xAxis: {
                categories: monthArr,
                plotBands: [{ // visualize the weekend
                    color: 'rgba(68, 170, 213, .2)'
                }],
                labels: {
                    style: {
                        color: colorfont,
                        cursor: "default",
                        fontSize: "10px"
                    }
                },
                min: 0
            },
            yAxis: {
                tickPositioner: function () {
                    var positions = [],
                        tick = Math.floor(Math.round(this.dataMin / 1000000) * 1000000),
                        increment = Math.abs(Math.ceil((Math.round(this.dataMax / 1000000) * 1000000 - tick) / 5));

                    if (this.dataMax !== null && this.dataMin !== null) {
                        for (tick; tick - increment <= this.dataMax; tick += increment) {
                            positions.push(tick);
                        }
                    }
                    return positions;
                },
                title:
                {
                    text: graph_HeaderDesc[0].desc_Monthly,
                    style: {
                        color: colorfont,
                        fontSize: "9px"
                    }
                },
                gridLineWidth: 0,
                labels: {
                    style: {
                        color: colorfont,
                        cursor: "default",
                        fontSize: "10px"
                    },
                    formatter: function () {
                        return this.value / 100000 + " " + graph_HeaderDesc[0].desc_Rs;
                    }
                }
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                areaspline: {
                    fillOpacity: 1.5
                }
            },
            tooltip: {
                formatter: function () {
                    return '' + this.series.name + '<br>: <b>' + numberWithCommas(this.y, 0, 0) + '</b>';
                }
            },

            series: [{
                name: graph_HeaderDesc[0].desc_Monthly,
                type: 'column',
                data: DataArr,
                color: 'rgba(114, 195, 240, 1)'
            }
            ]
        });
        $('#myChart_M').highcharts({
            chart: {
                height: (9 / 16 * 100) + '%',
                //type: gType,
                backgroundColor: backcolor,
                color: colorfont
            },
            title: {
                style: {
                    color: 'rgb(0, 0, 0)',
                    fontWeight: 'bold'
                },
                //x: titlePos,
                useHTML: true,
                text: '<div style="text-align:center;margin-right:100px;"></div>'
            },
            subtitle: {
                text: ''
            },
            exporting: {
                enabled: false
            },
            xAxis: {
                categories: monthArr,
                plotBands: [{ // visualize the weekend
                    color: 'rgba(68, 170, 213, .2)'
                }],
                labels: {
                    style: {
                        color: colorfont,
                        cursor: "default",
                        fontSize: "10px"
                    }
                },
                min: 0
            },
            yAxis: {
                tickPositioner: function () {
                    var positions = [],
                        tick = Math.floor(Math.round(this.dataMin / 1000000) * 1000000),
                        increment = Math.abs(Math.ceil((Math.round(this.dataMax / 1000000) * 1000000 - tick) / 5));

                    if (this.dataMax !== null && this.dataMin !== null) {
                        for (tick; tick - increment <= this.dataMax; tick += increment) {
                            positions.push(tick);
                        }
                    }
                    return positions;
                },
                title:
                {
                    text: graph_HeaderDesc[0].desc_Monthly,
                    style: {
                        color: colorfont,
                        fontSize: "9px"
                    }
                },
                gridLineWidth: 0,
                labels: {
                    style: {
                        color: colorfont,
                        cursor: "default",
                        fontSize: "10px"
                    },
                    formatter: function () {
                        return this.value / 100000 + " " + graph_HeaderDesc[0].desc_Rs;
                    }
                }
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                areaspline: {
                    fillOpacity: 1.5
                }
            },
            tooltip: {
                formatter: function () {
                    return '' + this.series.name + '<br>: <b>' + numberWithCommas(this.y, 0, 0) + '</b>';
                }
            },

            series: [{
                name: graph_HeaderDesc[0].desc_Monthly,
                type: 'column',
                data: DataArr,
                color: 'rgba(114, 195, 240, 1)'
            }
            ]
        });
    }
    else if (value == 2) {
        DataArr = dataArr_Y;
        var minval = 0;
        var maxval = Math.max.apply(null, DataArr);
        gType = 'column';
        $('#myChart').highcharts({
            chart: {
                height: (9 / 16 * 100) + '%',
                backgroundColor: backcolor,
                color: colorfont
            },
            title: {
                style: {
                    color: 'rgb(0, 0, 0)',
                    fontWeight: 'bold'
                },
                useHTML: true,
                text: '<div style="text-align:center;margin-right:100px;"></div>'
            },
            subtitle: {
                text: ''
            },
            exporting: {
                enabled: false
            },
            xAxis: {
                categories: yearArr,
                plotBands: [{ // visualize the weekend
                    color: 'rgba(68, 170, 213, .2)'
                }],
                labels: {
                    style: {
                        color: colorfont,
                        cursor: "default",
                        fontSize: "10px"
                    }
                },
                min: 0
            },
            yAxis: {
                min: 0,
                max: maxval,
                title:
                {
                    text: graph_HeaderDesc[0].desc_Monthly,
                    style: {
                        color: colorfont,
                        fontSize: "9px"
                    }
                },
                gridLineWidth: 0,
                labels: {
                    style: {
                        color: colorfont,
                        cursor: "default",
                        fontSize: "10px"
                    },
                    formatter: function () {
                        return this.value / 100000 + " " + graph_HeaderDesc[0].desc_Rs;
                    }
                }
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                areaspline: {
                    lineColor: 'pink'
                },
                series: {
                    pointWidth: 40
                }
            },
            tooltip: {
                formatter: function () {
                    return '' + this.series.name + ' ' + graph_HeaderDesc[0].desc_FinYear + ' ' + this.x + '<br>: <b>' + numberWithCommas(this.y, 0, 0) + '</b>';
                }
            },

            series: [{
                name: graph_HeaderDesc[0].desc_Monthly,
                type: 'column',
                data: DataArr,
                color: 'rgba(114, 195, 240, 1)'
            }
            ]
        });
        $('#myChart_M').highcharts({
            chart: {
                height: (9 / 16 * 100) + '%',
                backgroundColor: backcolor,
                color: colorfont
            },
            title: {
                style: {
                    color: 'rgb(0, 0, 0)',
                    fontWeight: 'bold'
                },
                useHTML: true,
                text: '<div style="text-align:center;margin-right:100px;"></div>'
            },
            subtitle: {
                text: ''
            },
            exporting: {
                enabled: false
            },
            xAxis: {
                categories: yearArr,
                plotBands: [{ // visualize the weekend
                    color: 'rgba(68, 170, 213, .2)'
                }],
                labels: {
                    style: {
                        color: colorfont,
                        cursor: "default",
                        fontSize: "10px"
                    }
                },
                min: 0
            },
            yAxis: {
                min: 0,
                max: maxval,
                title:
                {
                    text: graph_HeaderDesc[0].desc_Monthly,
                    style: {
                        color: colorfont,
                        fontSize: "9px"
                    }
                },
                gridLineWidth: 0,
                labels: {
                    style: {
                        color: colorfont,
                        cursor: "default",
                        fontSize: "10px"
                    },
                    formatter: function () {
                        return this.value / 100000 + " " + graph_HeaderDesc[0].desc_Rs;
                    }
                }
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                areaspline: {
                    lineColor: 'pink'
                },
                series: {
                    pointWidth: 40
                }
            },
            tooltip: {
                formatter: function () {
                    return '' + this.series.name + ' ' + graph_HeaderDesc[0].desc_FinYear + ' ' + this.x + '<br>: <b>' + numberWithCommas(this.y, 0, 0) + '</b>';
                }
            },

            series: [{
                name: graph_HeaderDesc[0].desc_Monthly,
                type: 'column',
                data: DataArr,
                color: 'rgba(114, 195, 240, 1)'
            }
            ]
        });
    }
};
function budjectsaction_chart(yearArr, dataArr_Y, Lang) {
    var backcolor = '#FFFFFF';
    var colorfont = '#000';
    var themeId = localStorage.getItem("themeId");
    if (typeof (themeId) == "undefined" || themeId == null) {
        themeId = 0;
    }
    if (themeId == 0) {
        backcolor = '#FFFFFF';
        colorfont = '#000';
    }
    else {
        backcolor = '#1e1e30';
        colorfont = '#f1f1f1';
    }
    var graph_HeaderDesc;
    if (Lang == 'hi') {
        graph_HeaderDesc = Graph_HeaderDesc_hi['Cat0']['SubCat0']['Param0'];
    }
    else {
        graph_HeaderDesc = Graph_HeaderDesc['Cat0']['SubCat0']['Param0'];
    }
    DataArr = dataArr_Y;
    var minval = 0;
    var maxval = Math.max.apply(null, DataArr);
    gType = 'column';
    $('#myChart_budjectsaction').highcharts({
        chart: {
            //height: (9 / 16 * 100) + '%',
            backgroundColor: backcolor,
            color: colorfont
        },
        title: {
            style: {
                color: 'rgb(0, 0, 0)',
                fontWeight: 'bold'
            },
            useHTML: true,
            text: '<div style="text-align:center;margin-right:100px;"></div>'
        },
        subtitle: {
            text: ''
        },
        exporting: {
            enabled: false
        },
        xAxis: {
            categories: yearArr,
            plotBands: [{ // visualize the weekend
                color: 'rgba(68, 170, 213, .2)'
            }],
            labels: {
                style: {
                    color: colorfont,
                    cursor: "default",
                    fontSize: "10px"
                }
            },
            min: 0
        },
        yAxis: {
            min: 0,
            max: maxval,
            title:
            {
                text: graph_HeaderDesc[0].desc_amount,
                style: {
                    color: colorfont,
                    fontSize: "9px"
                }
            },
            gridLineWidth: 0,
            labels: {
                style: {
                    color: colorfont,
                    cursor: "default",
                    fontSize: "10px"
                },
                formatter: function () {
                    return this.value + " " + graph_HeaderDesc[0].desc_Rs_Crore;
                }
            }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            areaspline: {
                lineColor: 'pink'
            },
            series: {
                pointWidth: 40
            }
        },
        tooltip: {
            formatter: function () {
                return '' + this.series.name + '<br>: <b>' + numberWithCommas(this.y, 0, 0) + '</b> ' + graph_HeaderDesc[0].desc_Rs_Crore;
            }
        },

        series: [{
            name: graph_HeaderDesc[0].desc_financial_progress,
            type: 'column',
            data: DataArr,
            color: 'rgba(114, 195, 240, 1)'
        }
        ]
    });
    $('#myChart_budjectsaction_M').highcharts({
        chart: {
            //height: (9 / 16 * 100) + '%',
            backgroundColor: backcolor,
            color: colorfont
        },
        title: {
            style: {
                color: 'rgb(0, 0, 0)',
                fontWeight: 'bold'
            },
            useHTML: true,
            text: '<div style="text-align:center;margin-right:100px;"></div>'
        },
        subtitle: {
            text: ''
        },
        exporting: {
            enabled: false
        },
        xAxis: {
            categories: yearArr,
            plotBands: [{ // visualize the weekend
                color: 'rgba(68, 170, 213, .2)'
            }],
            labels: {
                style: {
                    color: colorfont,
                    cursor: "default",
                    fontSize: "10px"
                }
            },
            min: 0
        },
        yAxis: {
            min: 0,
            max: maxval,
            title:
            {
                text: graph_HeaderDesc[0].desc_amount,
                style: {
                    color: colorfont,
                    fontSize: "9px"
                }
            },
            gridLineWidth: 0,
            labels: {
                style: {
                    color: colorfont,
                    cursor: "default",
                    fontSize: "10px"
                },
                formatter: function () {
                    return this.value + " " + graph_HeaderDesc[0].desc_Rs_Crore;
                }
            }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            areaspline: {
                lineColor: 'pink'
            },
            series: {
                pointWidth: 20
            }
        },
        tooltip: {
            formatter: function () {
                return '' + this.series.name + '' + this.x + '<br>: <b>' + numberWithCommas(this.y, 0, 0) + '</b> ' + graph_HeaderDesc[0].desc_Rs_Crore;
            }
        },

        series: [{
            name: graph_HeaderDesc[0].desc_financial_progress,
            type: 'column',
            data: DataArr,
            color: 'rgba(114, 195, 240, 1)'
        }
        ]
    });
}
function FHTC_Chart(stateArr, baseline010419_Arr, baseline010420_Arr, current20_21_Arr, achiveArr, remainArr, remain_15082019_Arr, achive_15082019_Arr, value, Lang, achive_M_Arr) {

    var graph_HeaderDesc;
    if (Lang == 'hi') {
        graph_HeaderDesc = Graph_HeaderDesc_hi['Cat0']['SubCat0']['Param0'];
    }
    else {
        graph_HeaderDesc = Graph_HeaderDesc['Cat0']['SubCat0']['Param0'];
    }
    if (value == 0) {
        $('#FHTC_Chart').highcharts({
            chart: {
                type: 'bar'
            },
            title: {
                text: '',//Comparative FHTC coverage status
                style: {
                    fontSize: "14px",
                    fontWeight: "900"
                }
            },
            xAxis: {
                categories: stateArr
            },
            tooltip: {
                formatter: function () {
                    return this.points.reduce(function (s, point) {
                        return s + '<br/>' + point.series.name + ': <b>' + numberWithCommas(point.y, 0, 0) + '</b> (' + parseFloat(point.percentage).toFixed(2) + '%)';
                    }, '<b>' + this.x + '</b>');
                },
                shared: true
            },
            yAxis: {
                min: 0,
                title: {
                    text: ''
                },
                tickInterval: 25,
                max: 100,
                labels: {
                    formatter: function () {
                        return this.axis.defaultLabelFormatter.call(this) + '%';
                    }
                }
            },
            exporting: {
                enabled: false
            },
            legend: {
                reversed: true
            },
            plotOptions: {
                series: {
                    stacking: 'percent',
                    events: {
                        legendItemClick: function () {
                            return false;
                        }
                    },
                    animation: false
                }
            },
            series: [{
                name: graph_HeaderDesc[0].desc_Series1,
                data: remainArr,
                color: '#E2E2E2',
                showInLegend: false
            },
            //{
            //    name: '15 Aug 2019',
            //    data: achive_15082019_Arr,
            //    color: '#FFFF00',
            //    showInLegend: false
            //},
            {
                name: graph_HeaderDesc[0].desc_Series2,
                data: achiveArr,
                color: '#3498DB',
                showInLegend: false
            }
            ]
        });
    }
    else {
        $('#FHTC_Chart').highcharts({
            chart: {
                type: 'bar'
            },
            title: {
                text: '',
                style: {
                    fontSize: "14px",
                    fontWeight: "900"
                }
            },
            xAxis: {
                categories: stateArr
            },
            tooltip: {
                formatter: function () {
                    return this.points.reduce(function (s, point) {
                        return s + '<br/>' + point.series.name + ': <b>' + numberWithCommas(point.y, 0, 0) + '</b> (' + parseFloat(point.percentage).toFixed(2) + '%)';
                    }, '<b>' + this.x + '</b>');
                },
                shared: true
            },
            yAxis: {
                min: 0,
                title: {
                    text: ''
                },
                tickInterval: 25,
                max: 100,
                labels: {
                    formatter: function () {
                        return this.axis.defaultLabelFormatter.call(this) + '%';
                    }
                }
            },
            exporting: {
                enabled: false
            },
            legend: {
                reversed: true
            },
            plotOptions: {
                series: {
                    stacking: 'percent',
                    events: {
                        legendItemClick: function () {
                            return false;
                        }
                    },
                    animation: false
                }
            },
            series: [{
                name: graph_HeaderDesc[0].desc_Series1,
                data: remain_15082019_Arr,
                color: '#E2E2E2',
                showInLegend: false
            },
            {
                name: graph_HeaderDesc[0].desc_Series2,
                data: achive_15082019_Arr,
                color: '#3498DB',
                showInLegend: false
            }]
        });
    }
}
function FHTC_Chart_info(stateArr, DataArr, FHTC_ChartId, color, statustype, Lang) {
    $('#' + FHTC_ChartId).highcharts({
        chart: {
            type: 'bar',
            backgroundColor: color,
            //height: (9 / 16 * 100) + '%',
        },
        title: {
            text: '',
            style: {
                fontSize: "14px",
                fontWeight: "900"
            }
        },
        xAxis: {
            categories: stateArr
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.x + '</b><br>' + this.series.name + ' : <b>' + numberWithCommas(this.y, 0, 0) + '</b>';
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: ''
            },
            labels: {
                formatter: function () {
                    return this.axis.defaultLabelFormatter.call(this);
                }
            }
        },
        exporting: {
            enabled: false
        },
        legend: {
            reversed: true
        },
        plotOptions: {
            series: {
                stacking: 'normal',
                pointWidth: 10
            }
        },
        series: [{
            name: '100 % FHTC ' + statustype,
            data: DataArr,
            color: '#006600',
            showInLegend: false
        }
        ]
    });
}

function villageSearch() {

    var StCode = $("#lblStateCode").text();
    var StName = $("#lblStateName").text();
    var DtCode = $("#lblDistrictCode").text();
    var DtName = $("#lblDistrictName").text();
    if (typeof StCode == 'undefined') {
        StCode = "0";
        StName = '';
    }
    if (typeof DtCode == 'undefined') {
        DtCode = "0";
        DtName = '';
    }
    if (StCode == '') {
        StCode = "0";
        StName = '';
    }
    if (DtCode == '') {
        DtCode = "0";
        DtName = '';
    }

    var tr_Search = '';
    var input, filter;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    if (filter.length > 0) {
        if (StCode == '0' && DtCode == '0') {
            //$("#myInput").attr("placeholder", "Search state ...");
            var obj = {};
            obj.StCode = encodeTxt(StCode);
            obj.Name = encodeTxt(filter);
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/JJM_StateDistrictSearch',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {
                    if (StCode == '0') {
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your state</b><i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="closetable()"></i></th>';
                        tr_Search += ' </tr> </thead>';
                    }
                    else {
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + StName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="removeStateSearch()"></i></div></th><tr>';
                        tr_Search += '<tr><th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your district</b></th>';
                        tr_Search += ' </tr> </thead>';
                    }
                    tr_Search += '<tbody><tr><td>';
                    for (var i = 0; i < data.d.length; i++) {
                        if (StCode == '0') {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataStateClick(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        else {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataDistrictClick(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        tr_Search += '' + toTitleCase(data.d[i].KeyName) + '</div>';
                    }
                    tr_Search += '</td></tr></tbody>';
                    $("#tbl_search").html("");
                    $("#tbl_search").append(tr_Search);
                    $("#tbl_search").show();
                }
            });
        }
        else if (StCode != '0' && DtCode == '0') {
            //$("#myInput").attr("placeholder", "Search district ...");
            var obj = {};
            obj.StCode = encodeTxt(StCode);
            obj.Name = encodeTxt(filter);
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/JJM_StateDistrictSearch',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {
                    if (StCode == '0') {
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your state</b><i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="closetable()"></i></th>';
                        tr_Search += ' </tr> </thead>';
                    }
                    else {
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + StName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="removeStateSearch()"></i></div></th><tr>';
                        tr_Search += '<tr><th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your district</b></th>';
                        tr_Search += ' </tr> </thead>';
                    }

                    tr_Search += '<tbody><tr><td>';
                    for (var i = 0; i < data.d.length; i++) {
                        if (StCode == '0') {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataStateClick(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        else {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataDistrictClick(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        tr_Search += '' + toTitleCase(data.d[i].KeyName) + '</div>';
                    }
                    tr_Search += '</td></tr></tbody>';
                    $("#tbl_search").html("");
                    $("#tbl_search").append(tr_Search);
                    $("#tbl_search").show();
                }
            });
        }
        else {
            //$("#myInput").attr("placeholder", "Search village ...");
            var obj = {};
            obj.VillageName = encodeTxt(filter);
            obj.StCode = encodeTxt(StCode);
            obj.DtCode = encodeTxt(DtCode);
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/Bind_search_Village',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {

                    if (data.d.length > 0) {
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border" colspan="3"><div class="jjm-padding jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label>' + StName + '</label></div><div class="jjm-padding jjm-border jjm-light-gray jjm-border-green jjm-card-2 jjm-round-large" style="margin-left: 6px !important;display:inline-block;"><label>' + DtName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor:pointer;" onclick="removeDistrictSearch()"></i></div></th></tr>';
                        tr_Search += '<th style="width:33%;" class="jjm-left-align jjm-padding"><b>Block</b></th>';
                        tr_Search += '<th style="width:33%;" class="jjm-left-align jjm-padding"><b>Panchayat</b></th>';
                        tr_Search += '<th style="width:33%;" class="jjm-left-align jjm-padding"><b>Village</b></th>';
                        tr_Search += ' </tr> </thead>';
                        tr_Search += '<tbody>';
                        for (var i = 0; i < data.d.length; i++) {
                            tr_Search += '<tr onclick="getdataVillageClick(' + "'" + (data.d[i].StCode).toString().trim() + "'" + ',' + "'" + (data.d[i].DtCode).toString().trim() + "'" + ',' + "'" + (data.d[i].VillageCode).toString().trim() + "'" + ',' + "'" + (data.d[i].VillageId).toString().trim() + "'" + ',' + "'" + toTitleCase(data.d[i].StateName) + "'" + ',' + "'" + toTitleCase(data.d[i].DistrictName) + "'" + ',' + "'" + toTitleCase(data.d[i].VillageName) + "'" + ')" style="cursor:pointer;">';
                            //tr_Search += '<td class="jjm-left-align jjm-border-top jjm-hide-large" style="width:100%;">' + toTitleCase(data.d[i].VillageNameAll) + '</td>';
                            tr_Search += '<td class="jjm-left-align jjm-border-top" style="width:33%;">' + toTitleCase(data.d[i].BlockName) + '</td>';

                            tr_Search += '<td class="jjm-left-align jjm-border-top" style="width:33%;">' + toTitleCase(data.d[i].PanchayatName) + '</td>';
                            tr_Search += '<td class="jjm-left-align jjm-border-top" style="width:33%;">' + toTitleCase(data.d[i].VillageName) + '</td>';
                            tr_Search += '</tr>';
                        }
                        tr_Search += '</tbody>';
                        $("#tbl_search").html("");
                        $("#tbl_search").append(tr_Search);
                        $("#tbl_search").show();
                    }
                    else {

                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border jjm-sand" colspan="3"><div class=" jjm-padding jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label>' + StName + '</label></div><div class="jjm-padding jjm-border jjm-light-gray jjm-border-green jjm-card-2 jjm-round-large" style="margin-left: 6px !important;display:inline-block;"><label>' + DtName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor:pointer;" onclick="removeDistrictSearch()"></i></div></th></tr>';
                        tr_Search += '<tr><th style="padding-left:35px;width:100%;" class="jjm-left-align jjm-border-top jjm-large"><b>No record found</b></th>';
                        tr_Search += ' </tr> </thead>';

                        $("#tbl_search").html("");
                        $("#tbl_search").append(tr_Search);
                        $("#tbl_search").show();
                    }
                }
            });
        }
    }
    else {
        if (StCode == '0' && DtCode == '0') {
            var obj = {};
            obj.StCode = encodeTxt(StCode);
            obj.Name = encodeTxt(filter);
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/JJM_StateDistrictSearch',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {
                    if (StCode == '0') {
                        //$("#myInput").attr("placeholder", "Search state ...");
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your state</b><i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="closetable()"></i></th>';
                        tr_Search += ' </tr> </thead>';
                    }
                    else {
                        //$("#myInput").attr("placeholder", "Search district ...");
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + StName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="removeStateSearch()"></i></div></th><tr>';
                        tr_Search += '<tr><th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your district</b></th>';
                        tr_Search += ' </tr> </thead>';
                    }

                    tr_Search += '<tbody><tr><td>';
                    for (var i = 0; i < data.d.length; i++) {
                        if (StCode == '0') {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataStateClick(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        else {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataDistrictClick(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        tr_Search += '' + toTitleCase(data.d[i].KeyName) + '</div>';
                    }
                    tr_Search += '</td></tr></tbody>';
                    $("#tbl_search").html("");
                    $("#tbl_search").append(tr_Search);
                    $("#tbl_search").show();
                }
            });
        }
        else if (StCode != '0' && DtCode == '0') {
            var obj = {};
            obj.StCode = encodeTxt(StCode);
            obj.Name = encodeTxt(filter);
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/JJM_StateDistrictSearch',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {
                    if (StCode == '0') {
                        //$("#myInput").attr("placeholder", "Search state ...");
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your state</b><i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="closetable()"></i></th>';
                        tr_Search += ' </tr> </thead>';
                    }
                    else {
                        //$("#myInput").attr("placeholder", "Search district ...");
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + StName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="removeStateSearch()"></i></div></th><tr>';
                        tr_Search += '<tr><th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your district</b></th>';
                        tr_Search += ' </tr> </thead>';
                    }

                    tr_Search += '<tbody><tr><td>';
                    for (var i = 0; i < data.d.length; i++) {
                        if (StCode == '0') {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataStateClick(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        else {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataDistrictClick(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        tr_Search += '' + toTitleCase(data.d[i].KeyName) + '</div>';
                    }
                    tr_Search += '</td></tr></tbody>';
                    $("#tbl_search").html("");
                    $("#tbl_search").append(tr_Search);
                    $("#tbl_search").show();
                }
            });
        }
        else {
            //$("#myInput").attr("placeholder", "Search village ...");
            tr_Search += '<thead><tr>';
            tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + StName + '</label></div><div class="jjm-padding-small jjm-border jjm-light-gray jjm-border-green jjm-card-2 jjm-round-large" style="margin-left: 6px !important;display:inline-block;"><label class="jjm-medium">' + DtName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor:pointer;" onclick="removeDistrictSearch()"></i></div></th></tr>';
            tr_Search += '<tr><th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>To search a village type first few letters of name of the village</b></th>';
            tr_Search += ' </tr> </thead>';
            tr_Search += '<tbody>';
            tr_Search += '<td class="jjm-left-align jjm-border-top" style="width:100%;"></td>';
            tr_Search += '</tr>';
            tr_Search += '</tbody>';
            $("#tbl_search").html("");
            $("#tbl_search").append(tr_Search);
            $("#tbl_search").show();
        }
    }
}
function getStateDistrict() {
    var StCode = $("#lblStateCode").text();
    var StName = $("#lblStateName").text();
    var DtCode = $("#lblDistrictCode").text();
    var DtName = $("#lblDistrictName").text();
    if (typeof StCode == 'undefined') {
        StCode = "0";
        StName = '';
    }
    if (typeof DtCode == 'undefined') {
        DtCode = "0";
        DtName = '';
    }
    if (StCode == '') {
        StCode = "0";
        StName = '';
    }
    if (DtCode == '') {
        DtCode = "0";
        DtName = '';
    }
    var tr_Search = '';
    if ((StCode != '0' && DtCode != '0')) {
        //$("#myInput").attr("placeholder", "Search village ...");
        tr_Search += '<thead><tr>';
        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + StName + '</label></div><div class="jjm-padding-small jjm-border jjm-light-gray jjm-border-green jjm-card-2 jjm-round-large" style="margin-left: 6px !important; display:inline-block;"><label class="jjm-medium">' + DtName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor:pointer;" onclick="removeDistrictSearch()"></i></div></th></tr>';
        tr_Search += '<tr><th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>To search a village type first few letters of name of the village</b></th>';
        tr_Search += ' </tr> </thead>';
        tr_Search += '<tbody>';
        tr_Search += '<td class="jjm-left-align jjm-border-top" style="width:100%;"></td>';
        tr_Search += '</tr>';
        tr_Search += '</tbody>';
    }
    else {
        var obj = {};
        obj.StCode = encodeTxt(StCode);
        obj.Name = encodeTxt('');
        $.ajax({
            type: 'POST',
            url: PageName + '.aspx/JJM_StateDistrictSearch',
            data: JSON.stringify(obj),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            async: false,
            success: function (data) {
                if (StCode == '0' || StCode == '') {
                    //$("#myInput").attr("placeholder", "Search state ...");
                    tr_Search += '<thead><tr>';
                    tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your state</b><i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="closetable()"></i></th>';
                    tr_Search += ' </tr> </thead>';
                }
                else {
                    //$("#myInput").attr("placeholder", "Search district ...");
                    tr_Search += '<thead><tr>';
                    tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + StName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="removeStateSearch()"></i></div></th><tr>';
                    tr_Search += '<tr><th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your district</b></th>';
                    tr_Search += ' </tr> </thead>';
                }

                tr_Search += '<tbody><tr><td>';
                for (var i = 0; i < data.d.length; i++) {
                    if (StCode == '0' || StCode == '') {
                        tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataStateClick(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';

                    }
                    else {
                        tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataDistrictClick(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                    }
                    tr_Search += '' + toTitleCase(data.d[i].KeyName) + '</div>';
                }
                tr_Search += '</td></tr></tbody>';
                $("#tbl_search").html("");
                $("#tbl_search").append(tr_Search);
                $("#tbl_search").show();
            }
        });
    }
}

//--------------Mobile search---
function villageSearch_M() {

    var StCode = $("#lblStateCode").text();
    var StName = $("#lblStateName").text();
    var DtCode = $("#lblDistrictCode").text();
    var DtName = $("#lblDistrictName").text();
    if (typeof StCode == 'undefined') {
        StCode = "0";
        StName = '';
    }
    if (typeof DtCode == 'undefined') {
        DtCode = "0";
        DtName = '';
    }
    if (StCode == '') {
        StCode = "0";
        StName = '';
    }
    if (DtCode == '') {
        DtCode = "0";
        DtName = '';
    }

    var tr_Search = '';
    var input_M, filter_M;
    input_M = document.getElementById("myInput_M");
    filter = input_M.value.toUpperCase();
    if (filter.length > 0) {
        if (StCode == '0' && DtCode == '0') {
            //$("#myInput").attr("placeholder", "Search state ...");
            var obj = {};
            obj.StCode = encodeTxt(StCode);
            obj.Name = encodeTxt(filter);
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/JJM_StateDistrictSearch',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {
                    if (StCode == '0') {
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your state</b><i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="closetable()"></i></th>';
                        tr_Search += ' </tr> </thead>';
                    }
                    else {
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + StName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="removeStateSearch_M()"></i></div></th><tr>';
                        tr_Search += '<tr><th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your district</b></th>';
                        tr_Search += ' </tr> </thead>';
                    }
                    tr_Search += '<tbody><tr><td>';
                    for (var i = 0; i < data.d.length; i++) {
                        if (StCode == '0') {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataStateClick_M(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        else {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataDistrictClick_M(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        tr_Search += '' + toTitleCase(data.d[i].KeyName) + '</div>';
                    }
                    tr_Search += '</td></tr></tbody>';
                    $("#tbl_search_M").html("");
                    $("#tbl_search_M").append(tr_Search);
                    $("#tbl_search_M").show();
                }
            });
        }
        else if (StCode != '0' && DtCode == '0') {
            //$("#myInput").attr("placeholder", "Search district ...");
            var obj = {};
            obj.StCode = encodeTxt(StCode);
            obj.Name = encodeTxt(filter);
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/JJM_StateDistrictSearch',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {
                    if (StCode == '0') {
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your state</b><i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="closetable()"></i></th>';
                        tr_Search += ' </tr> </thead>';
                    }
                    else {
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + StName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="removeStateSearch_M()"></i></div></th><tr>';
                        tr_Search += '<tr><th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your district</b></th>';
                        tr_Search += ' </tr> </thead>';
                    }

                    tr_Search += '<tbody><tr><td>';
                    for (var i = 0; i < data.d.length; i++) {
                        if (StCode == '0') {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataStateClick_M(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        else {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataDistrictClick_M(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        tr_Search += '' + toTitleCase(data.d[i].KeyName) + '</div>';
                    }
                    tr_Search += '</td></tr></tbody>';
                    $("#tbl_search_M").html("");
                    $("#tbl_search_M").append(tr_Search);
                    $("#tbl_search_M").show();
                }
            });
        }
        else {
            //$("#myInput").attr("placeholder", "Search village ...");
            var obj = {};
            obj.VillageName = encodeTxt(filter);
            obj.StCode = encodeTxt(StCode);
            obj.DtCode = encodeTxt(DtCode);
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/Bind_search_Village',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {

                    if (data.d.length > 0) {
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border" colspan="3"><div class="jjm-padding jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label>' + StName + '</label></div><div class="jjm-padding jjm-border jjm-light-gray jjm-border-green jjm-card-2 jjm-round-large" style="margin-left: 6px !important;display:inline-block;"><label>' + DtName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor:pointer;" onclick="removeDistrictSearch_M()"></i></div></th></tr>';
                        tr_Search += '<th style="width:33%;" class="jjm-left-align jjm-padding"><b>Block</b></th>';
                        tr_Search += '<th style="width:33%;" class="jjm-left-align jjm-padding"><b>Panchayat</b></th>';
                        tr_Search += '<th style="width:33%;" class="jjm-left-align jjm-padding"><b>Village</b></th>';
                        tr_Search += ' </tr> </thead>';
                        tr_Search += '<tbody>';
                        for (var i = 0; i < data.d.length; i++) {
                            tr_Search += '<tr onclick="getdataVillageClick(' + "'" + (data.d[i].StCode).toString().trim() + "'" + ',' + "'" + (data.d[i].DtCode).toString().trim() + "'" + ',' + "'" + (data.d[i].VillageCode).toString().trim() + "'" + ',' + "'" + (data.d[i].VillageId).toString().trim() + "'" + ',' + "'" + toTitleCase(data.d[i].StateName) + "'" + ',' + "'" + toTitleCase(data.d[i].DistrictName) + "'" + ',' + "'" + toTitleCase(data.d[i].VillageName) + "'" + ')" style="cursor:pointer;">';
                            //tr_Search += '<td class="jjm-left-align jjm-border-top jjm-hide-large" style="width:100%;">' + toTitleCase(data.d[i].VillageNameAll) + '</td>'
                            tr_Search += '<td class="jjm-left-align jjm-border-top" style="width:33%;">' + toTitleCase(data.d[i].BlockName) + '</td>';;
                            tr_Search += '<td class="jjm-left-align jjm-border-top" style="width:33%;">' + toTitleCase(data.d[i].PanchayatName) + '</td>';
                            tr_Search += '<td class="jjm-left-align jjm-border-top" style="width:33%;">' + toTitleCase(data.d[i].VillageName) + '</td>';
                            tr_Search += '</tr>';
                        }
                        tr_Search += '</tbody>';
                        $("#tbl_search_M").html("");
                        $("#tbl_search_M").append(tr_Search);
                        $("#tbl_search_M").show();
                    }
                    else {

                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border jjm-sand" colspan="3"><div class=" jjm-padding jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label>' + StName + '</label></div><div class="jjm-padding jjm-border jjm-light-gray jjm-border-green jjm-card-2 jjm-round-large" style="margin-left: 6px !important;display:inline-block;"><label>' + DtName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor:pointer;" onclick="removeDistrictSearch_M()"></i></div></th></tr>';
                        tr_Search += '<tr><th style="padding-left:35px;width:100%;" class="jjm-left-align jjm-border-top jjm-large"><b>No record found</b></th>';
                        tr_Search += ' </tr> </thead>';

                        $("#tbl_search_M").html("");
                        $("#tbl_search_M").append(tr_Search);
                        $("#tbl_search_M").show();
                    }
                }
            });
        }
    }
    else {
        if (StCode == '0' && DtCode == '0') {
            var obj = {};
            obj.StCode = encodeTxt(StCode);
            obj.Name = encodeTxt(filter);
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/JJM_StateDistrictSearch',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {
                    if (StCode == '0') {
                        //$("#myInput").attr("placeholder", "Search state ...");
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your state</b><i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="closetable()"></i></th>';
                        tr_Search += ' </tr> </thead>';
                    }
                    else {
                        //$("#myInput").attr("placeholder", "Search district ...");
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + StName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="removeStateSearch_M()"></i></div></th><tr>';
                        tr_Search += '<tr><th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your district</b></th>';
                        tr_Search += ' </tr> </thead>';
                    }

                    tr_Search += '<tbody><tr><td>';
                    for (var i = 0; i < data.d.length; i++) {
                        if (StCode == '0') {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataStateClick_M(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        else {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataDistrictClick_M(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        tr_Search += '' + toTitleCase(data.d[i].KeyName) + '</div>';
                    }
                    tr_Search += '</td></tr></tbody>';
                    $("#tbl_search_M").html("");
                    $("#tbl_search_M").append(tr_Search);
                    $("#tbl_search_M").show();
                }
            });
        }
        else if (StCode != '0' && DtCode == '0') {
            var obj = {};
            obj.StCode = encodeTxt(StCode);
            obj.Name = encodeTxt(filter);
            $.ajax({
                type: 'POST',
                url: PageName + '.aspx/JJM_StateDistrictSearch',
                data: JSON.stringify(obj),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                async: false,
                success: function (data) {
                    if (StCode == '0') {
                        //$("#myInput").attr("placeholder", "Search state ...");
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your state</b><i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="closetable()"></i></th>';
                        tr_Search += ' </tr> </thead>';
                    }
                    else {
                        //$("#myInput").attr("placeholder", "Search district ...");
                        tr_Search += '<thead><tr>';
                        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + StName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="removeStateSearch_M()"></i></div></th><tr>';
                        tr_Search += '<tr><th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your district</b></th>';
                        tr_Search += ' </tr> </thead>';
                    }

                    tr_Search += '<tbody><tr><td>';
                    for (var i = 0; i < data.d.length; i++) {
                        if (StCode == '0') {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataStateClick_M(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        else {
                            tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataDistrictClick_M(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                        }
                        tr_Search += '' + toTitleCase(data.d[i].KeyName) + '</div>';
                    }
                    tr_Search += '</td></tr></tbody>';
                    $("#tbl_search_M").html("");
                    $("#tbl_search_M").append(tr_Search);
                    $("#tbl_search_M").show();
                }
            });
        }
        else {
            //$("#myInput").attr("placeholder", "Search village ...");
            tr_Search += '<thead><tr>';
            tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + StName + '</label></div><div class="jjm-padding-small jjm-border jjm-light-gray jjm-border-green jjm-card-2 jjm-round-large" style="margin-left: 6px !important;display:inline-block;"><label class="jjm-medium">' + DtName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor:pointer;" onclick="removeDistrictSearch_M()"></i></div></th></tr>';
            tr_Search += '<tr><th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>To search a village type first few letters of name of the village</b></th>';
            tr_Search += ' </tr> </thead>';
            tr_Search += '<tbody>';
            tr_Search += '<td class="jjm-left-align jjm-border-top" style="width:100%;"></td>';
            tr_Search += '</tr>';
            tr_Search += '</tbody>';
            $("#tbl_search_M").html("");
            $("#tbl_search_M").append(tr_Search);
            $("#tbl_search_M").show();
        }
    }
}

function getStateDistrict_M() {
    var StCode = $("#lblStateCode").text();
    var StName = $("#lblStateName").text();
    var DtCode = $("#lblDistrictCode").text();
    var DtName = $("#lblDistrictName").text();
    if (typeof StCode == 'undefined') {
        StCode = "0";
        StName = '';
    }
    if (typeof DtCode == 'undefined') {
        DtCode = "0";
        DtName = '';
    }
    if (StCode == '') {
        StCode = "0";
        StName = '';
    }
    if (DtCode == '') {
        DtCode = "0";
        DtName = '';
    }
    var tr_Search = '';
    if ((StCode != '0' && DtCode != '0')) {
        //$("#myInput").attr("placeholder", "Search village ...");
        tr_Search += '<thead><tr>';
        tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + StName + '</label></div><div class="jjm-padding-small jjm-border jjm-light-gray jjm-border-green jjm-card-2 jjm-round-large" style="margin-left: 6px !important; display:inline-block;"><label class="jjm-medium">' + DtName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor:pointer;" onclick="removeDistrictSearch_M()"></i></div></th><tr>';
        tr_Search += ' </tr> </thead>';
        tr_Search += '<tbody>';
        tr_Search += '<td class="jjm-left-align jjm-border-top" style="width:100%;"></td>';
        tr_Search += '</tr>';
        tr_Search += '</tbody>';
    }
    else {
        var obj = {};
        obj.StCode = encodeTxt(StCode);
        obj.Name = encodeTxt('');
        $.ajax({
            type: 'POST',
            url: PageName + '.aspx/JJM_StateDistrictSearch',
            data: JSON.stringify(obj),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            async: false,
            success: function (data) {
                if (StCode == '0' || StCode == '') {
                    //$("#myInput").attr("placeholder", "Search state ...");
                    tr_Search += '<thead><tr>';
                    tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your state</b><i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="closetable()"></i></th>';
                    tr_Search += ' </tr> </thead>';
                }
                else {
                    //$("#myInput").attr("placeholder", "Search district ...");
                    tr_Search += '<thead><tr>';
                    tr_Search += '<th style="width:100%;" class="jjm-left-align jjm-padding jjm-border"><div class="jjm-padding-small jjm-border jjm-sand jjm-border-green jjm-card-2 jjm-round-large" style="display:inline-block;"><label class="jjm-medium">' + StName + '</label>&nbsp;<i class="fa fa-times-circle jjm-text-green jjm-right jjm-xlarge" aria-hidden="true" style="cursor: pointer;" onclick="removeStateSearch_M()"></i></div></th><tr>';
                    tr_Search += '<tr><th style="width:100%;" class="jjm-left-align jjm-padding jjm-large jjm-text-indigo"><b>Please select your district</b></th>';
                    tr_Search += ' </tr> </thead>';
                }

                tr_Search += '<tbody><tr><td>';
                for (var i = 0; i < data.d.length; i++) {
                    if (StCode == '0' || StCode == '') {
                        tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataStateClick_M(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';

                    }
                    else {
                        tr_Search += '<div class="jjm-col l6 m6 s6 jjm-border jjm-padding-small jjm-left-align" onclick="getdataDistrictClick_M(' + "'" + (data.d[i].KeyId).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyValue).toString().trim() + "'" + ',' + "'" + (data.d[i].KeyName).toString().trim() + "'" + ')" style="cursor:pointer;">';
                    }
                    tr_Search += '' + toTitleCase(data.d[i].KeyName) + '</div>';
                }
                tr_Search += '</td></tr></tbody>';
                $("#tbl_search_M").html("");
                $("#tbl_search_M").append(tr_Search);
                $("#tbl_search_M").show();
            }
        });
    }

}
//----------------List of Certified data------------------
function Bind_certified_District_Block(data, Cat, SubCat, Param, StCode, DtCode, Cer_Cat, Type, Lang) {
    var info_Section;
    var table_Header_desc;
    if (Lang == 'en') {
        info_Section = Section_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
        table_Header_desc = Table_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
    }
    else {
        info_Section = Section_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
        table_Header_desc = Table_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
    }
    $("#popHead").empty();
    if (Cer_Cat == 1) {
        $("#popHead").text(info_Section[0].desc_head_HGJ_dt_Certified);
    }
    else {
        $("#popHead").text(info_Section[0].desc_head_HGJ_bl_Certified);
    }
    var HH_Total = 0;
    var HC_Total = 0;
    var grapharray = data.d;
    var tr = "";

    tr += '<table class="jjm-table jjm-striped jjm-border">';
    tr += '<tbody><tr class="jjm-pale-blue jjm-text-black">';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_SNo_HGJCert + '</th>';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_stName_HGJ_Cert + '</th>';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_dtName_HGJ_Cert + '</th>';
    if (Cer_Cat == "1") {
    }
    else if (Cer_Cat == "2") {
        tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_blName_HGJ_Cert + '</th>';
    }
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_Households_HGJ_Cert + '</th>';
    tr += '</tr></tbody>';
    tr += '<tbody class="jjm-border">';
    for (var i = 0; i < grapharray.length; i++) {
        tr += '<tr class="item">';
        tr += '<td class="jjm-center jjm-border">' + grapharray[i].RowNo + '</div></td>';
        tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].StateName) + '</td>';
        tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].DistrictName) + '</td>';
        if (Cer_Cat == "1") {
        }
        else if (Cer_Cat == "2") {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].BlockName) + '</td>';
        }
        tr += '<td class="jjm-right-align jjm-border">' + numberWithCommas(grapharray[i].Households, 0, 0) + '</td>';
        tr += '</tr>';
        HH_Total += parseFloat(grapharray[i].Households);
    }
    tr += '</tbody>';
    tr += '<tfoot>';
    tr += '<tr style="font-weight:600;" class="jjm-light-gray">';
    tr += '<td class="jjm-right-align jjm-border"></td>';

    if (Cer_Cat == "1") {
        tr += '<td class="jjm-center jjm-border" colspan="2">' + table_Header_desc[0].desc_foot_total + '</td>';
    }
    else if (Cer_Cat == "2") {
        tr += '<td class="jjm-center jjm-border" colspan="3">' + table_Header_desc[0].desc_foot_total + '</td>';
    }
    tr += '<td class="jjm-right-align jjm-border">' + numberWithCommas(HH_Total, 0, 0) + '</td>';
    tr += '</tr>';
    tr += '</tfoot>';
    tr += '</table>';
    $("#tblcertified").empty();
    $("#tblcertified").append(tr);
    document.getElementById('ModelPop_Id').style.display = 'block'
}



//===================  //============ get HGJ Today List------ Anjeet

getHGJ_Today_list = function (Id) {
    var val = Id;
    if (val == 1) {
        var obj = {};
        obj.StCode11 = encodeTxt(G_StCode);
        $.ajax({
            type: 'POST',
            url: PageName + '.aspx/JJM_get_hgj_district',
            data: JSON.stringify(obj),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            //  async: false,
            beforeSend: function () {
                $(".se-pre-con").fadeIn("slow");
                $("#imgLoading3").fadeIn("slow");
            },
            success: function (data) {
                Bind_JJM_get_hgj_district(data, G_Cat, G_SubCat, G_Param, G_StCode, Lang);
            },
            complete: function () {
                $(".se-pre-con").fadeOut();
                $("#imgLoading3").fadeOut();
            }
        });
    } else if (val == 2) {
        var obj = {};
        obj.StCode11 = encodeTxt(G_StCode);
        obj.DtCode11 = encodeTxt(G_DtCode);
        $.ajax({
            type: 'POST',
            url: PageName + '.aspx/JJM_get_hgj_block',
            data: JSON.stringify(obj),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            // async: false,
            beforeSend: function () {
                $(".se-pre-con").fadeIn("slow");
                $("#imgLoading3").fadeIn("slow");
            },
            success: function (data) {
                Bind_JJM_get_hgj_block(data, G_Cat, G_SubCat, G_Param, G_StCode, Lang);
            },
            complete: function () {
                $(".se-pre-con").fadeOut();
                $("#imgLoading3").fadeOut();
            }
        });
    } else if (val == 3) {
        var obj = {};
        obj.StCode11 = encodeTxt(G_StCode);
        obj.DtCode11 = encodeTxt(G_DtCode);
        $.ajax({
            type: 'POST',
            url: PageName + '.aspx/JJM_get_hgj_Panchayat',
            data: JSON.stringify(obj),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            // async: false,
            beforeSend: function () {
                $(".se-pre-con").fadeIn("slow");
                $("#imgLoading3").fadeIn("slow");
            },
            success: function (data) {
                Bind_JJM_get_hgj_Panchayat(data, G_Cat, G_SubCat, G_Param, G_StCode, Lang);
            },
            complete: function () {
                $(".se-pre-con").fadeOut();
                $("#imgLoading3").fadeOut();
            }
        });
    } else if (val == 4) {
        var obj = {};
        obj.StCode11 = encodeTxt(G_StCode);
        obj.DtCode11 = encodeTxt(G_DtCode);
        $.ajax({
            type: 'POST',
            url: PageName + '.aspx/JJM_get_hgj_Village',
            data: JSON.stringify(obj),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            //async: false,
            beforeSend: function () {
                $(".se-pre-con").fadeIn("slow");
                $("#imgLoading3").fadeIn("slow");
            },
            success: function (data) {
                var dataInfo = data.d;
                var obj_HGJ_totalVill = {}, obj_HGJ_seven_days = {};
                if (dataInfo == "[]") {
                    Bind_JJM_get_hgj_Village(obj_HGJ_seven_days, obj_HGJ_totalVill, G_Cat, G_SubCat, G_Param, G_StCode, Lang);
                }
                else {
                    var result = dataInfo.slice(1, -1);
                    try {

                        obj_HGJ_seven_days = $.parseJSON(result.split(',[')[0]);
                        obj_HGJ_totalVill = $.parseJSON('[' + result.split(',[')[1]);

                        Bind_JJM_get_hgj_Village(obj_HGJ_seven_days, obj_HGJ_totalVill, G_Cat, G_SubCat, G_Param, G_StCode, Lang);
                    }
                    catch (err) {
                        Bind_JJM_get_hgj_Village(obj_HGJ_seven_days, obj_HGJ_totalVill, G_Cat, G_SubCat, G_Param, G_StCode, Lang);
                    }
                }

            },
            complete: function () {
                $(".se-pre-con").fadeOut();
                $("#imgLoading3").fadeOut();
            }
        });
    }
}

function Bind_JJM_get_hgj_district(data, Cat, SubCat, Param, StCode, Lang) {

    var info_Section;
    var table_Header_desc;
    if (Lang == 'en') {
        info_Section = Section_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
        table_Header_desc = Table_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
    }
    else {
        info_Section = Section_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
        table_Header_desc = Table_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
    }
    $("#popHGJdistrictHead").empty();
    $("#popHGJdistrictHead").text(info_Section[0].desc_head_hgj_district);

    var grapharray = data.d;
    var tr = "";

    tr += '<table class="jjm-table jjm-striped jjm-border">';
    tr += '<tbody><tr class="jjm-pale-blue jjm-text-black">';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_SNo_HGJCert + '</th>';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_stName_HGJ_Cert + '</th>';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_dtName_HGJ_Cert + '</th>';
    tr += '</tr></tbody>';
    tr += '<tbody class="jjm-border">';
    for (var i = 0; i < grapharray.length; i++) {
        tr += '<tr class="item">';
        tr += '<td class="jjm-center jjm-border" style="width:10px;">' + (parseInt(i) + 1) + '</td>';
        if (Lang == 'en') {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].StateName) + '</td>';
        }
        else {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].StateName_hi) + '</td>';
        }
        if (Lang == 'en') {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].DistrictName) + '</td>';
        }
        else {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].Districtname_hi) + '</td>';
        }
        tr += '</tr>';
    }
    tr += '</tbody>';
    tr += '</table>';
    $("#tblHGJdistrictdata").empty();
    $("#tblHGJdistrictdata").append(tr);

    document.getElementById('ModelHGJdistrictPop_Id').style.display = 'block'
}

function Bind_JJM_get_hgj_block(data, Cat, SubCat, Param, StCode, Lang) {
    var info_Section;
    var table_Header_desc;

    if (Lang == 'en') {
        info_Section = Section_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
        table_Header_desc = Table_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
    }
    else {
        info_Section = Section_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
        table_Header_desc = Table_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
    }

    $("#popHGJblockHead").empty();
    $("#popHGJblockHead").text(info_Section[0].desc_head_hgj_Block);

    var grapharray = data.d;
    var tr = "";

    tr += '<table class="jjm-table jjm-striped jjm-border">';
    tr += '<tbody><tr class="jjm-pale-blue jjm-text-black">';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_SNo_HGJCert + '</th>';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_stName_HGJ_Cert + '</th>';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_dtName_HGJ_Cert + '</th>';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_blName_HGJ_Cert + '</th>'

    tr += '</tr></tbody>';
    tr += '<tbody class="jjm-border">';
    for (var i = 0; i < grapharray.length; i++) {
        tr += '<tr class="item">';
        tr += '<td class="jjm-center-align jjm-border" style="width:10px;">' + (parseInt(i) + 1) + '</td>';
        if (Lang == 'en') {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].StateName) + '</td>';
        }
        else {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].StateName_hi) + '</td>';
        }
        if (Lang == 'en') {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].DistrictName) + '</td>';
        }
        else {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].Districtname_hi) + '</td>';
        }
        tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].BlockName) + '</td>';
        tr += '</tr>';
    }
    tr += '</tbody>';
    tr += '</table>';
    $("#tblHGJblockdata").empty();
    $("#tblHGJblockdata").append(tr);
    document.getElementById('ModelHGJblockPop_Id').style.display = 'block'
}

function Bind_JJM_get_hgj_Panchayat(data, Cat, SubCat, Param, StCode, Lang) {
    var info_Section;
    var table_Header_desc;

    if (Lang == 'en') {
        info_Section = Section_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
        table_Header_desc = Table_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
    }
    else {
        info_Section = Section_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
        table_Header_desc = Table_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
    }

    $("#popHGJpanchayatHead").empty();
    $("#popHGJpanchayatHead").text(info_Section[0].desc_head_hgj_gp);

    var grapharray = data.d;
    var tr = "";

    tr += '<table class="jjm-table jjm-striped jjm-border">';
    tr += '<tbody><tr class="jjm-pale-blue jjm-text-black">';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_SNo_HGJCert + '</th>';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_stName_HGJ_Cert + '</th>';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_dtName_HGJ_Cert + '</th>';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_blName_HGJ_Cert + '</th>'
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_GpName_HGJ_Cert + '</th>'
    tr += '</tr></tbody>';
    tr += '<tbody class="jjm-border">';
    for (var i = 0; i < grapharray.length; i++) {
        tr += '<tr class="item">';
        tr += '<td class="jjm-center-align jjm-border"  style="width:10px;">' + (parseInt(i) + 1) + '</td>';
        if (Lang == 'en') {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].StateName) + '</td>';
        }
        else {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].StateName_hi) + '</td>';
        }
        if (Lang == 'en') {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].DistrictName) + '</td>';
        }
        else {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].Districtname_hi) + '</td>';
        }
        tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].BlockName) + '</td>';
        tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].PanchayatName) + '</td>';
        tr += '</tr>';
    }
    tr += '</tbody>';
    tr += '</table>';
    $("#tblHGJpanchayatdata").empty();
    $("#tblHGJpanchayatdata").append(tr);
    document.getElementById('ModelHGJpanchayatPop_Id').style.display = 'block'
}

function Bind_JJM_get_hgj_Village(obj_HGJ_seven_days, obj_HGJ_totalVill, Cat, SubCat, Param, StCode, Lang) {

    var info_Section;
    var table_Header_desc;
    var noofvillage_hgj_seven_day = 0;
    if (Lang == 'en') {
        info_Section = Section_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
        table_Header_desc = Table_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
    }
    else {
        info_Section = Section_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
        table_Header_desc = Table_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
    }

    $("#popHGJVillageHead").empty();
    $("#popHGJVillageHead").text(info_Section[0].desc_head_hgj_village);

    var tr1 = "";
    tr1 += '<table class="jjm-table jjm-striped jjm-border">';
    tr1 += '<tbody><tr class="jjm-pale-blue jjm-text-black">';
    tr1 += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_SNo_HGJCert + '</th>';
    tr1 += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_stName_HGJ_Cert + '</th>';
    tr1 += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_dtName_HGJ_Cert + '</th>';
    tr1 += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_blName_HGJ_Cert + '</th>'
    tr1 += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_GpName_HGJ_Cert + '</th>'
    tr1 += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_VillageName_HGJ_Cert + '</th>'
    tr1 += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_Households_HGJ_Cert + '</th>'
    tr1 += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_HouseholdsConn_HGJ_Cert + '</th>'
    tr1 += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_Reported_Date_HGJ_Cert + '</th>'
    tr1 += '</tr></tbody>';
    tr1 += '<tbody class="jjm-border">';
    for (var i = 0; i < obj_HGJ_seven_days.length; i++) {
        tr1 += '<tr class="item">';
        tr1 += '<td class="jjm-centered jjm-padding-small jjm-border" style="width:4px;">' + (parseInt(i) + 1) + '</td>';
        if (Lang == 'en') {
            tr1 += '<td class="jjm-left-align jjm-padding-small jjm-border" style="width:13px;">' + toTitleCase(obj_HGJ_seven_days[i].StateName) + '</td>';
        }
        else {
            tr1 += '<td class="jjm-left-align jjm-padding-small jjm-border" style="width:13px;">' + toTitleCase(obj_HGJ_seven_days[i].StateName_hi) + '</td>';
        }
        if (Lang == 'en') {
            tr1 += '<td class="jjm-left-align jjm-padding-small jjm-border" style="width:13px;">' + toTitleCase(obj_HGJ_seven_days[i].Districtname) + '</td>';
        }
        else {
            tr1 += '<td class="jjm-left-align jjm-padding-small jjm-border" style="width:13px;">' + toTitleCase(obj_HGJ_seven_days[i].Districtname_hi) + '</td>';
        }
        tr1 += '<td class="jjm-left-align jjm-padding-small jjm-border" style="width:13px;">' + toTitleCase(obj_HGJ_seven_days[i].BlockName) + '</td>';
        tr1 += '<td class="jjm-left-align jjm-padding-small jjm-border" style="width:14px;">' + toTitleCase(obj_HGJ_seven_days[i].PanchayatName) + '</td>';
        tr1 += '<td class="jjm-left-align jjm-padding-small jjm-border" style="width:14px;">' + toTitleCase(obj_HGJ_seven_days[i].VillageName) + '</td>';
        tr1 += '<td class="jjm-left-align jjm-padding-small jjm-border" style="width:10px;">' + numberWithCommas(obj_HGJ_seven_days[i].Households, 0, 0) + '</td>';
        tr1 += '<td class="jjm-left-align jjm-padding-small jjm-border" style="width:13px;">' + numberWithCommas(obj_HGJ_seven_days[i].HouseConnection, 0, 0) + '</td>';
        tr1 += '<td class="jjm-left-align jjm-padding-small jjm-border" style="width:8px;">' + toTitleCase(obj_HGJ_seven_days[i].HGJReportedOn) + '</td>';
        tr1 += '</tr>';
        noofvillage_hgj_seven_day++;

    }



    tr1 += '</tbody>';
    tr1 += '</table>';
    $("#tblHGJvillagesevendaysdata").empty();
    $("#tblHGJvillagesevendaysdata").append(tr1);

    var date = obj_HGJ_seven_days[0].DateofYesturday;
    $("#txtdate").empty();
    $("#todate").empty();
    $("#txtdate").append(date);
    $("#todate").append(date);
    var Fdate = obj_HGJ_seven_days[0].DateofLastSevenDay;
    $("#Fdate").empty();
    $("#Fdate").append(Fdate);

    $("#hidCat_HGJ").val("0");
    $("#hidFdate").val(Fdate);
    $("#hidtodate").val(date);

    $("#lblnoofvillage_hgj_yesturday").empty();
    $("#lblnoofvillage_hgj_yesturday").append(numberWithCommas(obj_HGJ_totalVill[0].NoofvillageReported_Yesturday, 0, 0));

    $("#lblnoofvillage_hgj_seven_day").empty();
    $("#lblnoofvillage_hgj_seven_day").append(numberWithCommas(noofvillage_hgj_seven_day, 0, 0));

    document.getElementById('ModelHGJVillagePop_Id').style.display = 'block'
}

//===============end===============

//===================  //============ get HGJ Today Certified List------ Anjeet

getHGJ_Today_Certifiedlist = function (Id) {
    var val = Id;
    if (val == 1) {
        var obj = {};
        obj.StCode11 = encodeTxt(G_StCode);
        $.ajax({
            type: 'POST',
            url: PageName + '.aspx/JJM_get_hgjCertified_district',
            data: JSON.stringify(obj),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            //async: false,
            beforeSend: function () {
                $(".se-pre-con").fadeIn("slow");
                $("#imgLoading3").fadeIn("slow");
            },
            success: function (data) {
                Bind_JJM_get_hgjCertified_district(data, G_Cat, G_SubCat, G_Param, G_StCode, Lang);
            },
            complete: function () {
                $(".se-pre-con").fadeOut();
                $("#imgLoading3").fadeOut();
            }
        });
    } else if (val == 2) {
        var obj = {};
        obj.StCode11 = encodeTxt(G_StCode);
        obj.DtCode11 = encodeTxt(G_DtCode);
        $.ajax({
            type: 'POST',
            url: PageName + '.aspx/JJM_get_hgjCertified_block',
            data: JSON.stringify(obj),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            //    async: false,
            beforeSend: function () {
                $(".se-pre-con").fadeIn("slow");
                $("#imgLoading3").fadeIn("slow");
            },
            success: function (data) {
                Bind_JJM_get_hgjCertified_block(data, G_Cat, G_SubCat, G_Param, G_StCode, Lang);
            },
            complete: function () {
                $(".se-pre-con").fadeOut();
                $("#imgLoading3").fadeOut();
            }
        });
    } else if (val == 3) {
        var obj = {};
        obj.StCode11 = encodeTxt(G_StCode);
        obj.DtCode11 = encodeTxt(G_DtCode);
        $.ajax({
            type: 'POST',
            url: PageName + '.aspx/JJM_get_hgjCertified_Panchayat',
            data: JSON.stringify(obj),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            //async: false,
            beforeSend: function () {
                $(".se-pre-con").fadeIn("slow");
                $("#imgLoading3").fadeIn("slow");
            },
            success: function (data) {
                Bind_JJM_get_hgjCertified_Panchayat(data, G_Cat, G_SubCat, G_Param, G_StCode, Lang);
            },
            complete: function () {
                $(".se-pre-con").fadeOut();
                $("#imgLoading3").fadeOut();
            }
        });
    } else if (val == 4) {
        var obj = {};
        obj.StCode11 = encodeTxt(G_StCode);
        obj.DtCode11 = encodeTxt(G_DtCode);
        $.ajax({
            type: 'POST',
            url: PageName + '.aspx/JJM_get_hgjCertified_Village',
            data: JSON.stringify(obj),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            //    async: false,
            beforeSend: function () {
                $(".se-pre-con").fadeIn("slow");
                $("#imgLoading3").fadeIn("slow");
            },
            success: function (data) {
                var dataInfo = data.d;
                var obj_HGJ_seven_days = {};
                var obj_HGJ_ceritified_totalVill = {};
                if (dataInfo == "[]") {
                    Bind_JJM_get_hgjCertified_Village(obj_HGJ_seven_days, obj_HGJ_ceritified_totalVill, G_Cat, G_SubCat, G_Param, G_StCode, Lang);
                }
                else {
                    var result = dataInfo.slice(1, -1);
                    try {
                        obj_HGJ_seven_days = $.parseJSON(result.split(',[')[0]);
                        obj_HGJ_ceritified_totalVill = $.parseJSON('[' + result.split(',[')[1]);
                        Bind_JJM_get_hgjCertified_Village(obj_HGJ_seven_days, obj_HGJ_ceritified_totalVill, G_Cat, G_SubCat, G_Param, G_StCode, Lang);
                    }
                    catch (err) {
                        Bind_JJM_get_hgjCertified_Village(obj_HGJ_seven_days, obj_HGJ_ceritified_totalVill, G_Cat, G_SubCat, G_Param, G_StCode, Lang);
                    }
                }

            },
            complete: function () {
                $(".se-pre-con").fadeOut();
                $("#imgLoading3").fadeOut();
            }
        });
    }
}


function Bind_JJM_get_hgjCertified_district(data, Cat, SubCat, Param, StCode, Lang) {
    var info_Section;
    var table_Header_desc;
    if (Lang == 'en') {
        info_Section = Section_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
        table_Header_desc = Table_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
    }
    else {
        info_Section = Section_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
        table_Header_desc = Table_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
    }
    $("#popHGJdistrictHead").empty();
    $("#popHGJdistrictHead").text(info_Section[0].desc_head_hgjcertified_district);

    var grapharray = data.d;
    var tr = "";

    tr += '<table class="jjm-table jjm-striped jjm-border">';
    tr += '<tbody><tr class="jjm-pale-blue jjm-text-black">';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_SNo_HGJCert + '</th>';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_stName_HGJ_Cert + '</th>';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_dtName_HGJ_Cert + '</th>';
    tr += '</tr></tbody>';
    tr += '<tbody class="jjm-border">';
    for (var i = 0; i < grapharray.length; i++) {
        tr += '<tr class="item">';
        tr += '<td class="jjm-center jjm-border" style="width:10px;">' + (parseInt(i) + 1) + '</td>';
        if (Lang == 'en') {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].StateName) + '</td>';
        }
        else {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].StateName_hi) + '</td>';
        }
        if (Lang == 'en') {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].DistrictName) + '</td>';
        }
        else {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].Districtname_hi) + '</td>';
        }
        tr += '</tr>';
    }
    tr += '</tbody>';
    tr += '</table>';
    $("#tblHGJdistrictdata").empty();
    $("#tblHGJdistrictdata").append(tr);

    document.getElementById('ModelHGJdistrictPop_Id').style.display = 'block'
}

function Bind_JJM_get_hgjCertified_block(data, Cat, SubCat, Param, StCode, Lang) {
    var info_Section;
    var table_Header_desc;

    if (Lang == 'en') {
        info_Section = Section_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
        table_Header_desc = Table_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
    }
    else {
        info_Section = Section_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
        table_Header_desc = Table_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
    }

    $("#popHGJblockHead").empty();
    $("#popHGJblockHead").text(info_Section[0].desc_head_hgjcertified_Block);

    var grapharray = data.d;
    var tr = "";

    tr += '<table class="jjm-table jjm-striped jjm-border">';
    tr += '<tbody><tr class="jjm-pale-blue jjm-text-black">';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_SNo_HGJCert + '</th>';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_stName_HGJ_Cert + '</th>';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_dtName_HGJ_Cert + '</th>';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_blName_HGJ_Cert + '</th>'

    tr += '</tr></tbody>';
    tr += '<tbody class="jjm-border">';
    for (var i = 0; i < grapharray.length; i++) {
        tr += '<tr class="item">';
        tr += '<td class="jjm-center-align jjm-border" style="width:10px;">' + (parseInt(i) + 1) + '</td>';
        if (Lang == 'en') {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].StateName) + '</td>';
        }
        else {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].StateName_hi) + '</td>';
        }
        if (Lang == 'en') {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].DistrictName) + '</td>';
        }
        else {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].Districtname_hi) + '</td>';
        }
        tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].BlockName) + '</td>';
        tr += '</tr>';
    }
    tr += '</tbody>';
    tr += '</table>';
    $("#tblHGJblockdata").empty();
    $("#tblHGJblockdata").append(tr);
    document.getElementById('ModelHGJblockPop_Id').style.display = 'block'
}

function Bind_JJM_get_hgjCertified_Panchayat(data, Cat, SubCat, Param, StCode, Lang) {
    var info_Section;
    var table_Header_desc;

    if (Lang == 'en') {
        info_Section = Section_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
        table_Header_desc = Table_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
    }
    else {
        info_Section = Section_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
        table_Header_desc = Table_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
    }

    $("#popHGJpanchayatHead").empty();
    $("#popHGJpanchayatHead").text(info_Section[0].desc_head_hgjcertified_gp);

    var grapharray = data.d;
    var tr = "";

    tr += '<table class="jjm-table jjm-striped jjm-border">';
    tr += '<tbody><tr class="jjm-pale-blue jjm-text-black">';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_SNo_HGJCert + '</th>';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_stName_HGJ_Cert + '</th>';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_dtName_HGJ_Cert + '</th>';
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_blName_HGJ_Cert + '</th>'
    tr += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_GpName_HGJ_Cert + '</th>'
    tr += '</tr></tbody>';
    tr += '<tbody class="jjm-border">';
    for (var i = 0; i < grapharray.length; i++) {
        tr += '<tr class="item">';
        tr += '<td class="jjm-center-align jjm-border"  style="width:10px;">' + (parseInt(i) + 1) + '</td>';
        if (Lang == 'en') {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].StateName) + '</td>';
        }
        else {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].StateName_hi) + '</td>';
        }
        if (Lang == 'en') {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].DistrictName) + '</td>';
        }
        else {
            tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].Districtname_hi) + '</td>';
        }
        tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].BlockName) + '</td>';
        tr += '<td class="jjm-left-align jjm-border">' + toTitleCase(grapharray[i].PanchayatName) + '</td>';
        tr += '</tr>';
    }
    tr += '</tbody>';
    tr += '</table>';
    $("#tblHGJpanchayatdata").empty();
    $("#tblHGJpanchayatdata").append(tr);
    document.getElementById('ModelHGJpanchayatPop_Id').style.display = 'block'
}

function Bind_JJM_get_hgjCertified_Village(obj_HGJ_seven_days, obj_HGJ_ceritified_totalVill, Cat, SubCat, Param, StCode, Lang) {

    var info_Section;
    var table_Header_desc;
    var noofvillage_hgj_certified_seven_day = 0;
    if (Lang == 'en') {
        info_Section = Section_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
        table_Header_desc = Table_HeaderDesc['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
    }
    else {
        info_Section = Section_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
        table_Header_desc = Table_HeaderDesc_hi['Cat' + Cat]['SubCat' + SubCat]['Param' + Param];
    }
    $("#popHGJVillageHead").empty();
    $("#popHGJVillageHead").text(info_Section[0].desc_head_hgjcertified_village);

    var tr1 = "";
    tr1 += '<table class="jjm-table jjm-striped jjm-border">';
    tr1 += '<tbody><tr class="jjm-pale-blue jjm-text-black">';
    tr1 += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_SNo_HGJCert + '</th>';
    tr1 += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_stName_HGJ_Cert + '</th>';
    tr1 += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_dtName_HGJ_Cert + '</th>';
    tr1 += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_blName_HGJ_Cert + '</th>'
    tr1 += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_GpName_HGJ_Cert + '</th>'
    tr1 += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_VillageName_HGJ_Cert + '</th>'
    tr1 += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_Households_HGJ_Cert + '</th>'
    tr1 += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_HouseholdsConn_HGJ_Cert + '</th>'
    tr1 += '<th class="jjm-center jjm-padding jjm-border">' + table_Header_desc[0].desc_Certified_Date_HGJ_Cert + '</th>'
    tr1 += '</tr></tbody>';
    tr1 += '<tbody class="jjm-border">';
    for (var i = 0; i < obj_HGJ_seven_days.length; i++) {
        tr1 += '<tr class="item">';
        tr1 += '<td class="jjm-centered jjm-padding-small jjm-border" style="width:4px;">' + (parseInt(i) + 1) + '</td>';
        if (Lang == 'en') {
            tr1 += '<td class="jjm-left-align jjm-padding-small jjm-border" style="width:13px;">' + toTitleCase(obj_HGJ_seven_days[i].StateName) + '</td>';
        }
        else {
            tr1 += '<td class="jjm-left-align jjm-padding-small jjm-border" style="width:13px;">' + toTitleCase(obj_HGJ_seven_days[i].StateName_hi) + '</td>';
        }
        if (Lang == 'en') {
            tr1 += '<td class="jjm-left-align jjm-padding-small jjm-border" style="width:13px;">' + toTitleCase(obj_HGJ_seven_days[i].Districtname) + '</td>';
        }
        else {
            tr1 += '<td class="jjm-left-align jjm-padding-small jjm-border" style="width:13px;">' + toTitleCase(obj_HGJ_seven_days[i].Districtname_hi) + '</td>';
        }
        tr1 += '<td class="jjm-left-align jjm-padding-small jjm-border" style="width:13px;">' + toTitleCase(obj_HGJ_seven_days[i].BlockName) + '</td>';
        tr1 += '<td class="jjm-left-align jjm-padding-small jjm-border" style="width:14px;">' + toTitleCase(obj_HGJ_seven_days[i].PanchayatName) + '</td>';
        tr1 += '<td class="jjm-left-align jjm-padding-small jjm-border" style="width:14px;">' + toTitleCase(obj_HGJ_seven_days[i].VillageName) + '</td>';
        tr1 += '<td class="jjm-left-align jjm-padding-small jjm-border" style="width:10px;">' + numberWithCommas(obj_HGJ_seven_days[i].Households, 0, 0) + '</td>';
        tr1 += '<td class="jjm-left-align jjm-padding-small jjm-border" style="width:13px;">' + numberWithCommas(obj_HGJ_seven_days[i].HouseConnection, 0, 0) + '</td>';
        tr1 += '<td class="jjm-left-align jjm-padding-small jjm-border" style="width:8px;">' + toTitleCase(obj_HGJ_seven_days[i].HGJCertifiedOn) + '</td>';
        tr1 += '</tr>';
        noofvillage_hgj_certified_seven_day++;
    }
    tr1 += '</tbody>';
    tr1 += '</table>';

    var date = obj_HGJ_seven_days[0].DateofYesturday;
    $("#txtdate").empty();
    $("#todate").empty();
    $("#txtdate").append(date);
    $("#todate").append(date);
    var Fdate = obj_HGJ_seven_days[0].DateofLastSevenDay;
    $("#Fdate").empty();
    $("#Fdate").append(Fdate);

    $("#hidCat_HGJ").val("1");
    $("#hidFdate").val(Fdate);
    $("#hidtodate").val(date);

    $("#lblnoofvillage_hgj_yesturday").empty();
    $("#lblnoofvillage_hgj_yesturday").append(numberWithCommas(obj_HGJ_ceritified_totalVill[0].NoofvillageCertified_Yesturday, 0, 0));

    $("#lblnoofvillage_hgj_seven_day").empty();
    $("#lblnoofvillage_hgj_seven_day").append(numberWithCommas(noofvillage_hgj_certified_seven_day, 0, 0));

    $("#tblHGJvillagesevendaysdata").empty();
    $("#tblHGJvillagesevendaysdata").append(tr1);

    document.getElementById('ModelHGJVillagePop_Id').style.display = 'block'
}