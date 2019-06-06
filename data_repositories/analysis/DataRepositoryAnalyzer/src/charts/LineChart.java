package charts;

import org.knowm.xchart.demo.charts.ExampleChart;
import org.knowm.xchart.XYChart;
import org.knowm.xchart.XYChartBuilder;
import org.knowm.xchart.style.Styler.LegendPosition;
import org.knowm.xchart.style.markers.SeriesMarkers;
import org.knowm.xchart.XYSeries.XYSeriesRenderStyle;
import org.knowm.xchart.style.Styler;
import org.knowm.xchart.XYSeries;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Locale;

import org.knowm.xchart.VectorGraphicsEncoder;
import org.knowm.xchart.VectorGraphicsEncoder.VectorGraphicsFormat;


public class LineChart implements ExampleChart<XYChart> {
	private ArrayList<Integer> x;
	private HashMap<String, ArrayList<Integer>> ySeries;
	private String chartTitle;
	
	public LineChart(String chartTitle, ArrayList<Integer> x, HashMap<String, ArrayList<Integer>> ySeries) {
		super();
		this.x = x;
		this.ySeries = ySeries;
		this.chartTitle = chartTitle;
	}
		 
	//@Override
	public XYChart getChart() {
		 
		// Create Chart
		XYChart chart = new XYChartBuilder().width(800).height(600).title(this.chartTitle).xAxisTitle("year").yAxisTitle("number of datasets").build();
	 
		// Customize Chart
		chart.getStyler().setLegendPosition(LegendPosition.InsideNW);
		chart.getStyler().setDefaultSeriesRenderStyle(XYSeriesRenderStyle.Line);
		chart.getStyler().setYAxisLabelAlignment(Styler.TextAlignment.Right);
//		chart.getStyler().setYAxisDecimalPattern("$ #,###.##");
		chart.getStyler().setYAxisDecimalPattern("#,###.##");
		chart.getStyler().setXAxisDecimalPattern("####");
		chart.getStyler().setPlotMargin(0);
		chart.getStyler().setPlotContentSize(.95);
		chart.getStyler().setLocale(Locale.US);
		 
		for(String seriesName : this.ySeries.keySet()) {
	//		XYSeries seriesLiability = chart.addSeries("Liability", xAges, yLiability);
	//	    seriesLiability.setXYSeriesRenderStyle(XYSeries.XYSeriesRenderStyle.Area);
	//	    seriesLiability.setMarker(SeriesMarkers.NONE);
			
		    chart.addSeries(seriesName, this.x, this.ySeries.get(seriesName));
		}
		 
		return chart;
	}
	
}
