package data;

import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;

/**
 * Class representing a summary of a data repositories current state (available datasets and their properties).
 * 
 * @author klan_fi
 *
 */
public class RepositorySummary {
	private String repositoryName;	//repository name
	private ArrayList<String> standards;	//metadata standards considered in the repository
	private HashMap<String, DatasetSummary> data; //maps metadata standards to their dataset summaries
	
	/**
	 * Private constructor, shall not be used.
	 */
	private RepositorySummary() {
		super();
	}
	
	/**
	 * Creates and initializes a RepositorySummary object.
	 * 
	 * @param repositoryName	the name of the repository this summary refers to
	 */
	public RepositorySummary(String repositoryName) {
		
		super();
		
		//initialize variables
		this.repositoryName = repositoryName;
		this.standards = new ArrayList<String>();
		this.data = new HashMap<String, DatasetSummary>();

	}
	
	public boolean addMetadataStandard(String standard, DatasetSummary datasetSummary) {
		this.standards.add(standard);
		this.data.put(standard, datasetSummary);
		return true;
	}

	/**
	 * @return the repositoryName
	 */
	public String getRepositoryName() {
		return repositoryName;
	}

	/**
	 * @return the standards
	 */
	public ArrayList<String> getStandards() {
		return this.standards;
	}
	
	public boolean constainsStandard(String standardName) {
		if(this.standards.contains(standardName)) {
			return true;
		} else {
			return false;
		}
	}
	
	/**
	 * @return the dataset summary for each standard
	 */
	public HashMap<String, DatasetSummary> getDatasetSummaries() {
		return this.data;
	}
	
}
