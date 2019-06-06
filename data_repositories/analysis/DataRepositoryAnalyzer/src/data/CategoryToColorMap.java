package data;

import java.awt.Color;
import java.util.HashMap;
import java.util.TreeMap;

public class CategoryToColorMap {
	private static final TreeMap<Category, Color> colorMap;
	
	static {
		colorMap = new TreeMap<Category, Color>();
		colorMap.put(Category.ORGANISM, Color.RED);
		colorMap.put(Category.ENVIRONMENT, Color.GREEN);
		colorMap.put(Category.QUALITY, Color.ORANGE);
		colorMap.put(Category.MATERIAL, new Color(0,191,255));//light blue
		colorMap.put(Category.PROCESS, new Color(139,69,19));//brown
		colorMap.put(Category.METHOD, Color.YELLOW);
		colorMap.put(Category.TYPE, new Color(75,0,130));//purple
		colorMap.put(Category.ANATOMY, Color.LIGHT_GRAY);
		colorMap.put(Category.LOCATION, new Color(0,206,209)); //turquoise
		colorMap.put(Category.TIME, Color.BLUE);
		colorMap.put(Category.EVENT, new Color(189,183,107));//khaki
		colorMap.put(Category.PERSON, Color.PINK);
		colorMap.put(Category.HUMAN_INTERVENTION, Color.GRAY);
		colorMap.put(Category.NONE, Color.BLACK);
	}
	
	/**
	 * Returns the color for a given category.
	 * 
	 * @param category the given category
	 */
	public static Color getColor(Category category) {
		return colorMap.get(category);
	}
}
