package charts;

import java.util.ArrayList;
import java.util.Locale;
import java.util.TreeMap;
import java.awt.Color;

import org.knowm.xchart.CategoryChart;
import org.knowm.xchart.CategoryChartBuilder;
import org.knowm.xchart.demo.charts.ExampleChart;
import org.knowm.xchart.style.Styler.TextAlignment;

public class BarChart implements ExampleChart<CategoryChart> {
	private ArrayList<String> x;
	private TreeMap<String, ArrayList<Double>> y;
	private String chartTitle;
	private String xAxisTitle;
	private String yAxisTitle;
	private Color[] colorScheme;
	
	public BarChart(String chartTitle, String xAxisTitle, String yAxisTitle, ArrayList<String> x, TreeMap<String, ArrayList<Double>> y, Color[] colorScheme) {
		super();
		this.x = x;
		this.y = y;
		this.chartTitle = chartTitle;
		this.xAxisTitle = xAxisTitle;
		this.yAxisTitle = yAxisTitle;
		this.colorScheme = colorScheme;
	}


	//@Override
	public CategoryChart getChart() {

		// Create Chart
		CategoryChart chart = new CategoryChartBuilder().width(1500).height(600).title(this.chartTitle).xAxisTitle(this.xAxisTitle).yAxisTitle(this.yAxisTitle).build();

		// Customize Chart
//		chart.getStyler().setLegendPosition(LegendPosition.InsideNW);
		//if we have just one y-series
		if(this.y.size()==1) {
			chart.getStyler().setLegendVisible(false);
		//if we have more than one y-series
		} else {
			 chart.getStyler().setOverlapped(true);
		}
		
		chart.getStyler().setSeriesColors(colorScheme);
		chart.getStyler().setXAxisLabelRotation(90);
		chart.getStyler().setXAxisLabelAlignmentVertical(TextAlignment.Left);
		chart.getStyler().setLocale(Locale.US);
//		chart.getStyler().setAxisTickPadding(20);
		
		// Series
		for(String series : y.keySet()) {
			chart.addSeries(series.toString(), x, y.get(series));			
		}

		return chart;
	}
		  
}
