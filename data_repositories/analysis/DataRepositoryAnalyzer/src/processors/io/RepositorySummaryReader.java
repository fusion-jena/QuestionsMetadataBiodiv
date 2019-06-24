package processors.io;

import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;

import data.DatasetSummary;
import data.RepositorySummary;

/**
 * Class providing methods for reading repository summary data from a directory.
 * 
 * @author klan_fi
 *
 */
public class RepositorySummaryReader {
	
	public static ArrayList<RepositorySummary> readRepositorySummaries(String directoryName) {
		
		ArrayList<RepositorySummary> repositorySummaries = new ArrayList<RepositorySummary>();
		
//		String userDir = System.getProperty("user.dir");
		String fs = System.getProperty("file.separator");
//		String absoluteDirectoryPath = userDir + fs + directoryName;
//		File directory = new File(absoluteDirectoryPath);

		File directory = new File(directoryName);
		String[] repositoryDirs = directory.list();
		
		//for each subdirectory (each containing information of a certain data repository)
		for(String repositoryDirName : repositoryDirs) {
			
			//create a repository summary object
			File repositoryDir = new File(directoryName + fs + repositoryDirName);
			RepositorySummary repositorySummary = new RepositorySummary(repositoryDirName);
			
			//for each subdirectory (each containing information of a certain data standard) create and add a dataset summary
			String[] standardSubDirectories = repositoryDir.list();		
			for(String standardDirName : standardSubDirectories) {
				File standardDir = new File(directoryName + fs + repositoryDirName + fs + standardDirName);
				String[] csvFileNames = standardDir.list();
				String csvFilePath = directoryName + fs + repositoryDirName + fs + standardDirName + fs + csvFileNames[0];
				DatasetSummary datasetSummary = readDatasetSummary(csvFilePath);
				if(!(datasetSummary==null)) {
					repositorySummary.addMetadataStandard(standardDirName, datasetSummary);
					System.out.println("successfully added metadata standard " + standardDirName);
				} else {
					System.out.println("ERROR: Could not add metadata standard ...");
					return null;
				}
				
			}
			
			repositorySummaries.add(repositorySummary);
			System.out.println(repositorySummary.getStandards().toString());
			
		}

		return repositorySummaries;
		
	}
	
	/**
	 * Reads dataset information from a CSV file and stores them in dataset summary object.
	 * 
	 * @param fileName	the CSV file to read from
	 * @return	the dataset summary
	 */
	private static DatasetSummary readDatasetSummary(String fileName) {
		Reader in;
		int numColumns = 0;
		DatasetSummary datasetSummary = null;
		
		try {
			
			//read file
			in = new FileReader(fileName);
			System.out.println("Reading CSV-file " + fileName + " ...");
			Iterable<CSVRecord> records = CSVFormat.RFC4180.parse(in);

			int rowsWithoutDate = 0;
			int row = 0;
			int rowsWithZeroEntriesOnly = 0;
			int rowsWith_HeaderInDate = 0;
			
			int countValid =0;
			int countTotal =0;
			
			for (CSVRecord record : records) {
				
				//copy record entries into array list
				ArrayList<String> entriesAsList = new ArrayList<String>();
				for (String column : record) {
					entriesAsList.add(column);
				}
				numColumns = entriesAsList.size();
				
				//if we are processing the first row containing the headers
				if(row==0) {
					
					//create new dataset summary
					entriesAsList.remove(numColumns-1);
					entriesAsList.remove(0);
					System.out.println(entriesAsList.toString());
					datasetSummary = new DatasetSummary(entriesAsList);
					
				//if we are processing a data row
				} else {
					countTotal++;
					
					//add new dataset to dataset summary
					String datasetId = entriesAsList.get(0);
					String dateString = entriesAsList.get(entriesAsList.size()-1);
					Date creationDate = parseDate(dateString);
					
					//datasets without date are ignored
					if(creationDate!=null) {
						
						boolean allEntriesZero = true;
						ArrayList<Boolean> setDatasetAttributes = new ArrayList<Boolean>();
						for(int i=1; i < numColumns-1; i++) {
							int set = Integer.parseInt(entriesAsList.get(i));
							if(set==1) {
								setDatasetAttributes.add(true);
								
								allEntriesZero = false;
							} else {
								setDatasetAttributes.add(false);
							}			
						}
						
						//datasets with no attribute set are ignored
						if(!allEntriesZero) {
							
							if(!dateString.contains("_header")) {
								boolean success = datasetSummary.addEntry(datasetId, setDatasetAttributes, creationDate);
								countValid++;
								if(!success) { return null; }
							} else {
								rowsWith_HeaderInDate++;
							}
					
						} else {
							rowsWithZeroEntriesOnly++;
						}
					} else { rowsWithoutDate++;}
					
				}
				
				row++;
			}
			
			System.out.println("valid entries: " + countValid + " out of " + countTotal+ " total entries");
			System.out.println("Entries without date: " + rowsWithoutDate);
			System.out.println("Entries with all values set 0: " + rowsWithZeroEntriesOnly);
			System.out.println("Entries with _header in date: " + rowsWith_HeaderInDate);
			return datasetSummary;
			
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}
		
	}
	
	/**
	 * Parses a date string into a date object.
	 * 
	 * @param dateString	the date as string
	 * @return	the date object
	 */
	private static Date parseDate(String dateString) {
		
		SimpleDateFormat completeDateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
		SimpleDateFormat withoutTimeDateFormat = new SimpleDateFormat("yyyy-MM-dd");
		SimpleDateFormat justYearDateFormat = new SimpleDateFormat("yyyy");

		Date date = null;
		
		if(dateString.equals("-")) { return date; }
		
		try {
			date = completeDateFormat.parse(dateString);
			return date;
		} catch (ParseException e) {}
		
		try {
			date = justYearDateFormat.parse(dateString);
			return date;
		} catch (ParseException e) {}
		
		try {
			date = withoutTimeDateFormat.parse(dateString);
			return date;
		} catch (ParseException e) {}
		
		System.err.println("No known Date format found: " + dateString);
		return date;

	}
}