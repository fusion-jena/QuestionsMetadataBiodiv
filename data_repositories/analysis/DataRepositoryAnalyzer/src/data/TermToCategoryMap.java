package data;

import java.util.HashMap;

public class TermToCategoryMap {
	private static final HashMap<String, HashMap<String, Category>> termMap;
	
	static {
		termMap = new HashMap<String, HashMap<String, Category>>();
		
		//Dublin Core (oai_dc)
		//http://dublincore.org/documents/#recommendations
		//Metadata Encoding & Transmission Standard (mets)
		//http://www.loc.gov/standards/mets/
		//http://www.loc.gov/standards/mets/mets-schemadocs.html
		//Qualified Dublin Core Metadata (qdc)
		//http://dublincore.org/documents/2000/08/15/dcq-html/
		HashMap<String, Category> dcMap = new HashMap<String, Category>();
		dcMap.put("dc:coverage", Category.LOCATION);
		dcMap.put("dc:type", Category.TYPE);
		dcMap.put("dc:format", Category.TYPE);
		dcMap.put("dc:date", Category.TIME);
		dcMap.put("dc:contributor", Category.PERSON);
		dcMap.put("dc:creator", Category.PERSON);
        termMap.put("figshare.oai_dc", dcMap);
        termMap.put("gbif.oai_dc", dcMap);
        termMap.put("figshare.mets", dcMap);
        termMap.put("figshare.qdc", dcMap);
        termMap.put("pangaea.oai_dc", dcMap);
        termMap.put("dryad.oai_dc", dcMap);
        termMap.put("dryad.rdf", dcMap);
        termMap.put("zenodo.oai_dc", dcMap);
        
        //Datacite (datacite, datacite3, datacite4, oai_datacite, oai_datacite3)
        HashMap<String, Category> dciteMap = new HashMap<String, Category>();
        dciteMap.put("creator/creatorName", Category.PERSON);
        dciteMap.put("resourceTypeGeneral", Category.TYPE);
        dciteMap.put("geoLocation/contributorType", Category.PERSON);
        dciteMap.put("contributor/contributorName", Category.PERSON);
        dciteMap.put("formats/format", Category.TYPE);
        dciteMap.put("geoLocation/geoLocationPoint", Category.LOCATION);
        dciteMap.put("geoLocation/geoLocationBox", Category.LOCATION);
        termMap.put("figshare.oai_datacite", dciteMap);
        termMap.put("pangaea.datacite3", dciteMap);
        termMap.put("zenodo.datacite", dciteMap);
        termMap.put("zenodo.datacite3", dciteMap);
        termMap.put("zenodo.datacite4", dciteMap);
        termMap.put("zenodo.oai_datacite", dciteMap);
        termMap.put("zenodo.oai_datacite3", dciteMap);


        //Directory Interchange Format (dif)
        //https://gcmd.gsfc.nasa.gov/DocumentBuilder/defaultDif10/guide/index.html
        HashMap<String, Category> difMap = new HashMap<String, Category>();
        difMap.put("Data_Set_Citation/Dataset_Creator", Category.PERSON);
        difMap.put("Data_Set_Citation/Data_Presentation_Form", Category.TYPE);
        difMap.put("Temporal_Coverage/Start_Date", Category.TIME);
        difMap.put("Temporal_Coverage/Stop_Date", Category.TIME);  
        difMap.put("Spatial_Coverage/Southernmost_Latitude", Category.LOCATION);
        difMap.put("Spatial_Coverage/Northernmost_Latitude", Category.LOCATION);
        difMap.put("Spatial_Coverage/Westernmost_Longitude", Category.LOCATION);
        difMap.put("Spatial_Coverage/Easternmost_Longitude", Category.LOCATION);
        difMap.put("Personnel/First_Name", Category.PERSON);
        difMap.put("Personnel/Last_Name", Category.PERSON);
        difMap.put("Personnel/Email", Category.PERSON);
        difMap.put("Personnel/Phone", Category.PERSON);
        difMap.put("Contact_Address/Address", Category.PERSON);
        difMap.put("Contact_Address/Personnel/City", Category.PERSON);
        difMap.put("Contact_Address/Province_or_State", Category.PERSON);
        difMap.put("Contact_Address/Postal_Code", Category.PERSON);
        difMap.put("Contact_Address/Country", Category.PERSON);
        difMap.put("Distribution/Distribution_Media", Category.TYPE);
        difMap.put("Distribution/Distribution_Size", Category.TYPE);
        difMap.put("Distribution/Distribution_Format", Category.TYPE);
        difMap.put("Spatial_Coverage/Minimum_Depth", Category.LOCATION);
        difMap.put("Spatial_Coverage/Maximum_Depth", Category.LOCATION);
        difMap.put("Spatial_Coverage/Minimum_Altitude", Category.LOCATION);
        difMap.put("Spatial_Coverage/Maximum_Altitude", Category.LOCATION);
        difMap.put("Parameters/Detailed_Variable", Category.QUALITY);
        difMap.put("Sensor_Name/Long_Name", Category.METHOD);
        
        
        termMap.put("pangaea.dif", difMap);
        
        //ISO 19139 (iso19139)
        //https://inspire.ec.europa.eu/file/1705/download?token=iSTwpRWd
        HashMap<String, Category> isoMap = new HashMap<String, Category>();
        isoMap.put("CI_Address/electronicMailAddress/gco:CharacterString", Category.PERSON);
        isoMap.put("CI_ResponsibleParty/individualName/gco:CharacterString", Category.PERSON);
        isoMap.put("CI_ResponsibleParty/organizationName/gco:CharacterString", Category.PERSON);
        isoMap.put("CI_Date/date/gco:DateTime", Category.TIME);
        isoMap.put("CI_Date/date/gco:Date", Category.TIME);
        isoMap.put("extent/gml:TimePeriod/gml:beginPosition", Category.TIME);
        isoMap.put("extent/gml:TimePeriod/gml:endPosition", Category.TIME);
        
        isoMap.put("EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal", Category.LOCATION);
        isoMap.put("EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal", Category.LOCATION);
        isoMap.put("EX_GeographicBoundingBox/gmd:southBoundLatidue/gco:Decimal", Category.LOCATION);
        isoMap.put("EX_GeographicBoundingBox/gmd:northBoundLatidue/gco:Decimal", Category.LOCATION);
        
        isoMap.put("MD_Format/name/gco:CharacterString", Category.TYPE);
        
        
        isoMap.put("MD_CoverageDescription/attributeDescription/gco:RecordType", Category.QUALITY);
        isoMap.put("units/gml:UnitDefinition/gml:name", Category.QUALITY);
        
        isoMap.put("MD_Band/descriptor/gco:CharacterString", Category.METHOD);
        
        termMap.put("pangaea.iso19139", isoMap);
        termMap.put("pangaea.iso19139.iodp", isoMap);
        
        //PANGAEA XML schema (pan_md)
        //https://wiki.pangaea.de/wiki/PANGAEA_XML_schema
        //https://wiki.pangaea.de/wiki/Data_model
        //http://ws.pangaea.de/schemas/pangaea/MetaData.xsd
        HashMap<String, Category> panMap = new HashMap<String, Category>();
        panMap.put("md:author/md:lastName", Category.PERSON);
        panMap.put("md:author/md:firstName", Category.PERSON);
        panMap.put("md:author/md:eMail", Category.PERSON);
        panMap.put("md:author/md:orcid", Category.PERSON);
        panMap.put("md:PI/md:lastName", Category.PERSON);
        panMap.put("md:PI/md:firstName", Category.PERSON);
        panMap.put("md:PI/md:URI", Category.PERSON);
        panMap.put("md:PI/md:orcid", Category.PERSON);
        //panMap.put("md:year", Category.TIME); citation
        //panMap.put("md:dateTime", Category.TIME); citation
        
        panMap.put("md:temporal/md:minDateTime", Category.TIME);
        panMap.put("md:temporal/md:maxDateTime", Category.TIME);
        panMap.put("md:event/md:dateTime", Category.TIME);
        panMap.put("md:event/md:dateTime2", Category.TIME);
        
        panMap.put("md:geographic/md:westBoundLongitude", Category.LOCATION);
        panMap.put("md:geographic/md:eastBoundLongitude", Category.LOCATION);
        panMap.put("md:geographic/md:southBoundLatitude", Category.LOCATION);
        panMap.put("md:geographic/md:northBoundLatitude", Category.LOCATION);
        panMap.put("md:geographic/md:meanLongitude", Category.LOCATION);
        panMap.put("md:geographic/md:meanLatitude", Category.LOCATION);
        panMap.put("md:event/md:longitude", Category.LOCATION);
        panMap.put("md:event/md:latitude", Category.LOCATION);
        panMap.put("md:event/md:longitude2", Category.LOCATION);
        panMap.put("md:event/md:latitude2", Category.LOCATION);
        panMap.put("md:event/md:elevation", Category.LOCATION);
        panMap.put("md:event/md:elevation2", Category.LOCATION);
        panMap.put("md:elevation/md:min", Category.LOCATION);
        panMap.put("md:elevation/md:max", Category.LOCATION);
        
        panMap.put("format", Category.TYPE);
        
        panMap.put("md:parameter/md:name", Category.QUALITY);
        panMap.put("md:parameter/md:shortName", Category.QUALITY);
        panMap.put("md:parameter/md:unit", Category.QUALITY);
        panMap.put("md:matrixColumn/md:comment", Category.QUALITY);
        
        panMap.put("md:device/md:name", Category.METHOD);
        panMap.put("md:device/md:optionalLabel", Category.METHOD);
        panMap.put("md:method/md:name", Category.METHOD);
        panMap.put("md:method/md:URI", Category.METHOD);
        
        termMap.put("pangaea.pan_md", panMap);
        
        //Ecological Metadata Language (eml)
        //http://www.dcc.ac.uk/resources/metadata-standards/eml-ecological-metadata-language
        //https://knb.ecoinformatics.org/external//emlparser/docs/eml-2.1.1/index.html
        //http://www.gbif.jp/v2/pdf/gbif_metadata_profile_guide_en_v1.pdf
        HashMap<String, Category> emlMap = new HashMap<String, Category>();
        emlMap.put("individualName/givenName", Category.PERSON);
        emlMap.put("individualName/surName", Category.PERSON);
        emlMap.put("creator/organizationName", Category.PERSON);
        emlMap.put("personnel/organizationName", Category.PERSON);
        emlMap.put("individualName/positionName", Category.PERSON);
        emlMap.put("personnel/positionName", Category.PERSON);
        emlMap.put("address/deliveryPoint", Category.PERSON);
        emlMap.put("address/city", Category.PERSON);
        emlMap.put("address/administrativeArea", Category.PERSON);
        emlMap.put("address/postalCode", Category.PERSON);
        emlMap.put("address/country", Category.PERSON);
        emlMap.put("contact/phone", Category.PERSON);
        emlMap.put("metadataProvider/electronicMadatilAddress", Category.PERSON);
        emlMap.put("associatedParty/electronicMadatilAddress", Category.PERSON);
        emlMap.put("personnel/electronicMadatilAddress", Category.PERSON);
        emlMap.put("associatedParty/role", Category.PERSON);
        emlMap.put("address", Category.PERSON);
        emlMap.put("associatedParty", Category.PERSON);
        emlMap.put("geographicCoverage/geographicDescription", Category.LOCATION);
        emlMap.put("boundingCoordinates/westBoundingCoordinate", Category.LOCATION);
        emlMap.put("boundingCoordinates/eastBoundingCoordinate", Category.LOCATION);
        emlMap.put("boundingCoordinates/northBoundingCoordinate", Category.LOCATION);
        emlMap.put("boundingCoordinates/southBoundingCoordinate", Category.LOCATION);
        emlMap.put("beginDate/calendarDate", Category.TIME);
        emlMap.put("endDate/calendarDate", Category.TIME);
        emlMap.put("coverage/temporalCoverage", Category.TIME);
        emlMap.put("taxonomicCoverage/generalTaxonomicCoverage", Category.ORGANISM);
        emlMap.put("taxonomicClassification/taxonRankName", Category.ORGANISM);
        emlMap.put("taxonomicClassification/taxonRankValue", Category.ORGANISM);
        emlMap.put("taxonomicClassification/commonName", Category.ORGANISM);
        emlMap.put("dataset/methods", Category.METHOD);
        emlMap.put("description/para", Category.METHOD); // sometimes also ENVIRONMENT information
        emlMap.put("samplingDescription/para", Category.METHOD);      // sometimes also ENVIRONMENT information
        emlMap.put("gbif/specimenPreservationMethod", Category.METHOD);
        emlMap.put("coverage", Category.LOCATION);
        emlMap.put("externallyDefinedFormat/formatName", Category.TYPE);
        emlMap.put("externallyDefinedFormat/formatVersion", Category.TYPE);
        emlMap.put("physical/characterEncoding", Category.TYPE);
        emlMap.put("gbif/livingTimePeriod", Category.TIME);
        emlMap.put("jgtiCuratorialUnit/beginRange", Category.TIME);
        emlMap.put("jgtiCuratorialUnit/endRange", Category.TIME);
        emlMap.put("descriptor/descriptorValue", Category.ENVIRONMENT);
        
        termMap.put("gbif.eml", emlMap);
        
        //Common European Research Information Format (cerif)
        //http://www.dcc.ac.uk/resources/metadata-standards/cerif-common-european-research-information-format
        //https://www.eurocris.org/Uploads/Web%20pages/CERIF-1.3/Specifications/CERIF1.3_FDM.pdf
        HashMap<String, Category> cerifMap = new HashMap<String, Category>();
        cerifMap.put("cerif:cfPersId", Category.PERSON);
        cerifMap.put("cerif:cfPersName", Category.PERSON);
        cerifMap.put("cerif:cfName", Category.PERSON);
        termMap.put("figshare.cerif", cerifMap);
        
        //Figshare Resource Description Framework (rdf)
        HashMap<String, Category> rdfMap = new HashMap<String, Category>();
        rdfMap.put("rdf:about", Category.PERSON);
        rdfMap.put("vcard:givenName", Category.PERSON);
        rdfMap.put("vcard:familyName", Category.PERSON);
        termMap.put("figshare.rdf", rdfMap);
        
        //Metadata Object Description Schema (mods)
        //http://www.loc.gov/standards/mods/
        HashMap<String, Category> modsMap = new HashMap<String, Category>();
        modsMap.put("mods:publisher", Category.PERSON);
        modsMap.put("mods:geographic", Category.LOCATION);
        modsMap.put("mods:temporal", Category.TIME);
        termMap.put("dryad.mets", modsMap);
        
        //Dryad ore (ore)
        //Zenodo marc21
        //Zenodo marcxml
        HashMap<String, Category> oreMap = new HashMap<String, Category>();
        termMap.put("dryad.ore", oreMap);
        termMap.put("zenodo.marc21", oreMap);        
        termMap.put("zenodo.marcxml", oreMap);        
    }
	
	/**
	 * Returns the category for a given standard and term.
	 * @param standard	the given standard
	 * @param term	the given term
	 */
	public static Category getCategory(String standard, String term) {
		//System.out.println(term);
		Category category = termMap.get(standard).get(term);
		if(category==null) {
			return Category.NONE;
		} else {
			return category;
		}
	}
}
