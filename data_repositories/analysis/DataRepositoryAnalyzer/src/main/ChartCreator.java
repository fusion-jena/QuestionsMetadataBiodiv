package main;

import processors.io.RepositorySummaryReader;

import java.awt.Color;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.TreeMap;

import org.knowm.xchart.BitmapEncoder;
import org.knowm.xchart.BitmapEncoder.BitmapFormat;
import org.knowm.xchart.CategoryChart;
import org.knowm.xchart.VectorGraphicsEncoder;
import org.knowm.xchart.VectorGraphicsEncoder.VectorGraphicsFormat;
import org.knowm.xchart.XYChart;
import org.knowm.xchart.demo.charts.ExampleChart;
import org.knowm.xchart.demo.charts.line.LineChart01;

import charts.BarChart;
import charts.LineChart;
import data.Category;
import data.CategoryToColorMap;
import data.DatasetSummary;
import data.RepositorySummary;
import data.TermToCategoryMap;


public class ChartCreator {

	//set path to metadata directory
	public static String metadataPath = "C:\\Daten\\phd\\fusionBiodivQuestions\\data_repositories\\metadata";
	//set path to output directory
	public static String outputPath = "C:\\Daten\\phd\\questions\\analysis-metadata-friederike\\DataRepositoryAnalyzer\\charts";
	
	public static void main(String[] args) {
		
		//read repository statistics from CSV-file
		ArrayList<RepositorySummary> repositorySummaries = RepositorySummaryReader.readRepositorySummaries(metadataPath);
		System.out.println("REPOSITORIES RED ...");
		
		/**
		 * DATASETS PER YEAR
		 */
		plotDatasetsPerYear(repositorySummaries);
		
		
		/**
		 * PORTION OF ATTRIBUTES FILLED
		 */
		plotPortionOfAttributesFilled(repositorySummaries, true);
		
		/**
		 * PORTION OF ATTRIBUTES FILLED BY YEAR
		 */
		//plotPortionOfAttributesFilledByYear(repositorySummaries);
		
	}
	
	/**
	 * Plots the number of datasets per year.
	 * 
	 * @param repositorySummaries the underlying repository statistics to use
	 */
	private static void plotDatasetsPerYear(ArrayList<RepositorySummary> repositorySummaries) {
//		HashMap<String, ArrayList<Double>> ySeries = new HashMap<String, ArrayList<Double>>();
		HashMap<String, TreeMap<Integer, Integer>> ySeries = new HashMap<String, TreeMap<Integer, Integer>>();
		int minYear = 5000;
		int maxYear = 0;
		int numOfDatsetsWithErroneousDates = 0;
		
		//for each repository and standard, calculate datasets per year
		for(RepositorySummary repositorySummary : repositorySummaries) {
			
			String repositoryName = repositorySummary.getRepositoryName();
			
			//for each standard
			HashMap<String, DatasetSummary> datasetSummaries = repositorySummary.getDatasetSummaries();
			for(String standard : datasetSummaries.keySet()) {
				
				System.out.println("Statistics for " + repositoryName + "." + standard);
				
				//get datasets per year
				DatasetSummary datasetSummary = datasetSummaries.get(standard);
				System.out.println("# of datasets: " + datasetSummary.getNumberOfDatsets());
				ArrayList<Date> creationDates = datasetSummary.getCreationDates();
				TreeMap<Integer, Integer> datasetsPerYear = new TreeMap<Integer, Integer>();
				for(Date date : creationDates) {
					Calendar calendar = Calendar.getInstance();
					calendar.setTime(date);
					int year = calendar.get(Calendar.YEAR);
					
					//CHANGE HERE, IF YOU WANT TO RESTRICT DATES, also necessary to remove unusually high or low years due to wrong date entries
//					if(year>=1500 && year<2020) {
					if(year>=2000 || year<1000) {
						numOfDatsetsWithErroneousDates++;
					}
					
					if(year>=2000 && year<2020) {
						if(year<minYear) { minYear = year; }
						if(year>maxYear) { maxYear = year; }
						
						if(datasetsPerYear.containsKey(year)) {
							datasetsPerYear.replace(year, datasetsPerYear.get(year) + 1);
						} else {
							datasetsPerYear.put(year, 1);
						}
					}
				}
				
				System.out.println("Datsets per year: " + datasetsPerYear);
				
				//add the series for plotting
				ySeries.put(repositoryName + "." + standard, datasetsPerYear);
				System.out.println("minYear:" + minYear);
				System.out.println("maxYear:" + maxYear);
				System.out.println("# of datasets with erroneous date: " + numOfDatsetsWithErroneousDates);
			}
		}
			
		//determine x values (covering the range [minYear,maxYear])
		ArrayList<Integer> x = new ArrayList<Integer>();
		for(int i=minYear; i<=maxYear; i++) {
			x.add(i);
		}
		
		//complete the y series (add a 0 dataset count for each year not appearing in the series) and add them for plotting
		HashMap<String, ArrayList<Integer>> ySeriesCompleted = new HashMap<String, ArrayList<Integer>>();
		
		//for each series
		for(String seriesName : ySeries.keySet()) {
			TreeMap<Integer, Integer> series = ySeries.get(seriesName);
			
			//for each year
			for(Integer year : x) {
				if(!series.containsKey(year)) {
					series.put(year, 0);
				}
			}
			
			ySeriesCompleted.put(seriesName, new ArrayList<Integer>(series.values()));
		}
		
//		System.out.println("ySeriesCompleted: " + ySeriesCompleted.toString());
		
		//plot datasets per year	
		String firstRepositoryName = repositorySummaries.get(0).getRepositoryName();
		
		ExampleChart<XYChart> exampleChart = new LineChart(firstRepositoryName + ": number of datasets per year", x, ySeriesCompleted);
		XYChart chart = exampleChart.getChart();
		try {
//		    BitmapEncoder.saveBitmapWithDPI(chart, "./Sample_Chart_300_DPI", BitmapFormat.PNG, 300);
//	    	VectorGraphicsEncoder.saveVectorGraphic(chart, "./Sample_Chart", VectorGraphicsFormat.SVG);
			System.out.println("plotting ...");
			VectorGraphicsEncoder.saveVectorGraphic(chart, outputPath + "/" + firstRepositoryName + "-datasets-per-year", VectorGraphicsFormat.EPS);
		    BitmapEncoder.saveBitmapWithDPI(chart, outputPath + "/" + firstRepositoryName + "-datasets-per-year", BitmapFormat.PNG, 300);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}
	
	/**
	 * Plots for each field of a metadata standard and repository, the percentage of datasets where this field is filled.  
	 * 
	 * @param repositorySummaries the underlying repository statistics to use
	 * @param categoryColorScheme the color scheme for the categories to use
	 */
	private static void plotPortionOfAttributesFilled(ArrayList<RepositorySummary> repositorySummaries, boolean categoryColorScheme) {
		
		//for each repository and standard, calculate datasets per year
		for(RepositorySummary repositorySummary : repositorySummaries) {
			
			String repositoryName = repositorySummary.getRepositoryName();
			
			//for each standard
			HashMap<String, DatasetSummary> datasetSummaries = repositorySummary.getDatasetSummaries();
			for(String standard : datasetSummaries.keySet()) {
				
				//get datasets per year
				DatasetSummary datasetSummary = datasetSummaries.get(standard);
				ArrayList<String> attributes = datasetSummary.getAttributes();
				
				//REMOVE, IF YOU WANT TO SEE THE FULL ATTRIBUTE PATH
				//shorten attribute names
				ArrayList<String> attributesShort = new ArrayList<String>();
				for(String attribute : attributes) {
					String[] splittedTerm = attribute.split("/");
					String term = splittedTerm[splittedTerm.length-1];
					
					
					// in ISO use the last two preceding terms (usually long path length)
					if(standard.equals("iso19139") || standard.equals("iso19139.iodp")){
						if ((splittedTerm.length-2)>0){
							//System.out.println(standard);
							String precedingTerm1 = splittedTerm[splittedTerm.length-2];
							//String precedingTerm2= splittedTerm[splittedTerm.length-3];
							//attributesShort.add(precedingTerm2+"/"+precedingTerm1+"/"+term);
							attributesShort.add(precedingTerm1+"/"+term);
						}else{
							attributesShort.add(term);
						}
						
					}
					else if(standard.equals("rdf") || standard.equals("oai_dc") || standard.equals("qdc")|| standard.equals("ore")){
						attributesShort.add(term);
					}
					else if((splittedTerm.length-2)>0){
						String precedingTerm = splittedTerm[splittedTerm.length-2];
						attributesShort.add(precedingTerm+"/"+term);
					}else{
						attributesShort.add(term);
					}
				}
				
				ArrayList<Double> portions = new ArrayList<Double>();
				for(String attribute : attributes) {
					portions.add(datasetSummary.getPortionSet(attribute));
				}
						
				//remove attributes never filled
				ArrayList<String> x = new ArrayList<String>();
				ArrayList<Double> y = new ArrayList<Double>();
				for(int i=0; i<attributes.size(); i++) {
					if(portions.get(i)!=0.0) {
						//REPLACE BY x.add(attributes.get(i)); IF YOU WANT LONG ATTRIBUTE NAMES
						x.add(attributesShort.get(i));
						y.add(portions.get(i));
					}
				}
				
				//plot
				ExampleChart<CategoryChart> exampleChart;
				TreeMap<String, ArrayList<Double>> series = new TreeMap<String, ArrayList<Double>>();
				series.put("portion", y);
				Color[] colorScheme;
				//if we use a color scheme with increasing intensity for each y-series
				if(!categoryColorScheme) {
					colorScheme = createIncreasingColorScheme(y.size());
					exampleChart = new BarChart(repositoryName + "." + standard + ": portion of attributes set", "attributes", "% of attributes filled", x, series, colorScheme);
				//if we use a color per category
				} else {
					//make a y-series per category (this is necessary, since XYChart cannot color values of a single y-series differently)
					TreeMap<Category, ArrayList<Double>> paddedSeries = new TreeMap<Category, ArrayList<Double>>();
					for(int i=0; i<x.size(); i++) {
						
//						String termLong = x.get(i);
//						String[] splittedTerm = termLong.split("/");
//						String term = splittedTerm[splittedTerm.length-1];
						Category category = TermToCategoryMap.getCategory(repositoryName + "." + standard, x.get(i));
						
						if( paddedSeries.containsKey(category) ) {
							paddedSeries.get(category).set(i, y.get(i));
						} else {
							ArrayList<Double> newYSeries = new ArrayList<Double>();
							for(int j=0; j<x.size(); j++) {
								newYSeries.add(0.0);
							}
							newYSeries.set(i, y.get(i));
							paddedSeries.put(category, newYSeries);
						}	
					}
															
					colorScheme = createCategoryColorScheme(paddedSeries);
					
					//copy y-series in a map with categories as string
					TreeMap<String, ArrayList<Double>> paddedSeriesWithStringKey = new TreeMap<String, ArrayList<Double>>();
					for(Category category : paddedSeries.keySet()) {
						paddedSeriesWithStringKey.put(category.toString(), paddedSeries.get(category));
					}
					
					exampleChart = new BarChart(repositoryName + "." + standard + ": portion of attributes set", "attributes", "% of attributes filled", x, paddedSeriesWithStringKey, colorScheme);
				}
					
				
				CategoryChart chart = exampleChart.getChart();
				try {
					System.out.println("plotting ...");
					if(datasetSummary.getCreationDates().size()==0) {
						System.out.println("NO (ACCURATE) DATASETS IN REPOSITORY LEFT. WILL NOT CREATE PLOT!");
					} else {
						VectorGraphicsEncoder.saveVectorGraphic(chart, outputPath + "/" + repositoryName + "-" + standard + "-attributes-set", VectorGraphicsFormat.EPS);
					    BitmapEncoder.saveBitmapWithDPI(chart, outputPath + "/" + repositoryName + "-" + standard + "-attributes-set", BitmapFormat.PNG, 300);						
					}

				} catch (IOException e) {
					e.printStackTrace();
				}

			}
		}
		
	}
	
	/**
     * Plots for each field of a metadata standard and repository, the percentage of datasets where this field is filled splitted by year (given with each dataset).  
	 * 
	 * @param repositorySummaries the underlying repository statistics to use
	 */
	private static void plotPortionOfAttributesFilledByYear(ArrayList<RepositorySummary> repositorySummaries) {
		
		//for each repository and standard, calculate datasets per year
		for(RepositorySummary repositorySummary : repositorySummaries) {
			
			String repositoryName = repositorySummary.getRepositoryName();
			
			//for each standard
			HashMap<String, DatasetSummary> datasetSummaries = repositorySummary.getDatasetSummaries();
			for(String standard : datasetSummaries.keySet()) {
				
				//get datasets per year
				DatasetSummary datasetSummary = datasetSummaries.get(standard);
				ArrayList<String> attributes = datasetSummary.getAttributes();
				
				//get minYear, maxYear and portions by attribute
				HashMap<String, HashMap<Integer, Double>> portionsByAttribute = new HashMap<String, HashMap<Integer, Double>>();
				int minYear = 5000;
				int maxYear = 0;
				for(String attribute : attributes) {
					HashMap<Integer, Double> portionByYear = datasetSummary.getPortionSetByYear(attribute);
					portionsByAttribute.put(attribute, portionByYear);
					for(Integer year : portionByYear.keySet()) {
						if(year<minYear) { minYear = year; }
						if(year>maxYear) { maxYear = year; }
					}
				}
				
				//initialize portions by year considering all years in [minyear, maxYear]
				TreeMap<String, ArrayList<Double>> portionsByYear = new TreeMap<String, ArrayList<Double>>();
				for(int i=minYear; i<=maxYear; i++) {
					ArrayList<Double> portions = new ArrayList<Double>();
					for(String attribute : attributes) {
						portions.add(0.0);
					}
					portionsByYear.put(Integer.valueOf(i).toString(), portions);
				}
				
				for(String attribute : portionsByAttribute.keySet()) {
					HashMap<Integer, Double> portions = portionsByAttribute.get(attribute);
					for(Integer year : portions.keySet()) {
						ArrayList<Double> portionsOfYear = portionsByYear.get(year.toString());
						portionsOfYear.set(attributes.indexOf(attribute), portions.get(year));
						portionsByYear.replace(year.toString(), portionsOfYear);
					}	
				}
				
//				//remove attributes never filled
//				ArrayList<String> x = new ArrayList<String>();
//				ArrayList<Double> y = new ArrayList<Double>();
//				for(int i=0; i<attributes.size(); i++) {
//					if(portions.get(i)!=0.0) {
//						x.add(attributes.get(i));
//						y.add(portions.get(i));
//					}
//				}
				
				//plot
				ExampleChart<CategoryChart> exampleChart = new BarChart("Portion of attributes set by year", "attributes", "% of attributes filled", attributes, portionsByYear, createIncreasingColorScheme(1));
				CategoryChart chart = exampleChart.getChart();
				try {
					System.out.println("plotting ...");
//					VectorGraphicsEncoder.saveVectorGraphic(chart, outputPath + "/" + repositoryName + "-" + standard + "-attributes-set-by-year", VectorGraphicsFormat.PDF);
				    BitmapEncoder.saveBitmapWithDPI(chart, outputPath + "/" + repositoryName + "-" + standard + "-attributes-set-by-year", BitmapFormat.PNG, 300);
				    VectorGraphicsEncoder.saveVectorGraphic(chart, outputPath + "/" + repositoryName + "-" + standard + "-attributes-set-by-year", VectorGraphicsFormat.EPS);
				} catch (IOException e) {
					e.printStackTrace();
				}

			}
		}
		
	}

	/**
	 * Returns a color scheme of blue with increasing intensity.
	 * 
	 * @param numOfColors	number of colors to generate
	 * @return	the color scheme
	 */
	private static Color[] createIncreasingColorScheme(int numOfColors) {
		Color[] colorScheme = new Color[numOfColors];
		int offset = (int) Math.floor( 255.0 / (double) numOfColors );
		for(int i=0; i< colorScheme.length; i++) {
			colorScheme[i] = new Color(0, 0, offset * (i + 1) );
		}
		return colorScheme;
	}
	
	/**
	 * Returns a color scheme with the corresponding category color for each term.
	 * 
	 * @param categoryToSeriesMap	the categories to series map
	 * @return	the color scheme
	 */
	private static Color[] createCategoryColorScheme(TreeMap<Category, ArrayList<Double>> categoryToSeriesMap) {
		Color[] colorScheme = new Color[categoryToSeriesMap.keySet().size()];
		int i=0;
		
		TreeMap<String, Category> categoryToCategoryString = new TreeMap<String, Category>();
		for(Category category : categoryToSeriesMap.keySet()) {
			categoryToCategoryString.put(category.toString(), category);
		}
		
		for(String categoryString : categoryToCategoryString.keySet()) {
			colorScheme[i] = CategoryToColorMap.getColor( categoryToCategoryString.get(categoryString) );
			i++;
		}
						
		return colorScheme;
	}
}