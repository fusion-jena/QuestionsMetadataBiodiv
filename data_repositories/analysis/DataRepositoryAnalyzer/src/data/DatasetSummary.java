package data;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;

/**
 * Class representing information about datasets and their characteristics.
 * 
 * @author klan_fi
 *
 */
public class DatasetSummary {
	
	private ArrayList<String> datasetIds;	//the ids of the datasets for which information has been stored in this summary
	private ArrayList<String> attributes;	//the metadata attributes which might be set in a dataset's metadata
	private HashMap<String, Integer> attributeIds; //maps attribute names to ids
	private ArrayList<ArrayList<Boolean>> setAttributes;	//set/not set information for each attribute and dataset
	private int setAttributesSize;
	private ArrayList<Date> creationDates;	//the creation dates of the datasets for which information has been stored in this summary
	
	/**
	 * Private constructor, shall not be used.
	 */
	private DatasetSummary() {
		super();
	}
	
	/**
	 * Creates and initializes a DatasetSummary object.
	 * 
	 * @param attributes	the list of metadata attributes, which might be set in a dataset 
	 */
	public DatasetSummary(ArrayList<String> attributes) {
		
		super();
		
		//initialize variables
		this.datasetIds = new ArrayList<String>();
		this.attributes = attributes;
		this.attributeIds = new HashMap<String, Integer>();
		for(int i=0; i<this.attributes.size(); i++) {
			this.attributeIds.put(this.attributes.get(i), i);
		}
//		System.out.println("Attributes to IDs: " + this.attributeIds.toString());
		this.setAttributes = new ArrayList<ArrayList<Boolean>>();
		setAttributesSize = attributes.size();
		this.creationDates = new ArrayList<Date>();
		
	}
	
	public boolean addEntry(String datasetId, ArrayList<Boolean> setDatasetAttributes, Date creationDate) {
		
		//the number of attributes in the entry fits the number of attributes considered in this summary
		if(setDatasetAttributes.size()==this.setAttributesSize) {	
			this.datasetIds.add(datasetId);
			this.setAttributes.add(setDatasetAttributes);
			this.creationDates.add(creationDate);
			return true;
		//the number of attributes in the entry does not fit the number of attributes considered in this summary
		} else {
			return false;
		}
		
	}

	public ArrayList<Date> getCreationDates() {
		return this.creationDates;
	}
	
	public ArrayList<String> getAttributes() {
		return attributes;
	}
	
	/**
	 * Returns the percentage of datasets where the given attribute is set (i.e. filled).
	 * 
	 * @param	attribute	the given attribute
	 * @return	the percentage of datasets where the attribute is set
	 */
	public double getPortionSet(String attribute) {
		int numSetAttributes = 0;
		for(int i=0; i<this.setAttributes.size(); i++) {
			boolean set = this.setAttributes.get(i).get(this.attributeIds.get(attribute));
			if(set) { numSetAttributes++; }
		}

		//if there are no datasets available, set portion to 0.0
		if(this.setAttributes.size()==0) {
			return 0.0;
		} else {
			return ( (double) numSetAttributes / (double) this.setAttributes.size() );
		}
		
	}
	
	/**
	 * Returns the percentage of datasets where the given attribute is set (i.e. filled) by year.
	 * 
	 * @param	attribute	the given attribute
	 * @return	the percentage of datasets where the attribute is set by year
	 */
	public HashMap<Integer, Double> getPortionSetByYear(String attribute) {
		HashMap<Integer, Double> setCountByYear = new HashMap<Integer, Double>();
		HashMap<Integer, Double> totalCountByYear = new HashMap<Integer, Double>();
		for(int i=0; i<this.setAttributes.size(); i++) {
			Date date = this.creationDates.get(i);
			boolean set = this.setAttributes.get(i).get(this.attributeIds.get(attribute));
			Calendar calendar = Calendar.getInstance();
			calendar.setTime(date);
			int year = calendar.get(Calendar.YEAR);

			if(setCountByYear.containsKey(year)) {
				if(set) {
					double count = setCountByYear.get(year) + 1.0;
					setCountByYear.replace(year, count);
				}
				double totalCount = totalCountByYear.get(year) + 1.0;
				totalCountByYear.replace(year, totalCount);
			} else {
				if(set) {
					setCountByYear.put(year, 1.0);
				}
				totalCountByYear.put(year, 1.0);
			}
		}
		
		//determine portions from counts
		HashMap<Integer, Double> portionByYear = new HashMap<Integer, Double>();
		for(Integer year : totalCountByYear.keySet()) {
			double totalCount = totalCountByYear.get(year);
			if(setCountByYear.containsKey(year)) {
				double setCount = setCountByYear.get(year);
				portionByYear.put(year, setCount / totalCount);
			} else {
				portionByYear.put(year, 0.0);
			}
		}
		return portionByYear;
	}
	
	/**
	 * Returns the number of datasets contained in this dataset summary.
	 * 
	 * @return the number of datasets
	 */
	public int getNumberOfDatsets() {
		return this.datasetIds.size();
	}

}
