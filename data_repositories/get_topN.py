import argparse
import pandas as pd
import traceback


parser = argparse.ArgumentParser(description="Get top N used keywords in repository CSV file")
parser.add_argument("-c", "--csv", help="Set the path to CSV file", required=True)
parser.add_argument("-n", "--number", help="Set number of keywords (-1 = all)", required=True, type=int)
args = parser.parse_args()

try:
    csv_data = pd.read_csv(args.csv, sep=",", header=0, encoding="utf-8")
    csv_data.sort_values(by="count", ascending=False, inplace=True)
    top_N = csv_data[:args.number]
    print(top_N.to_string(index=False), end="\n\n")
    top_N_output = args.csv.replace(".csv", "_getTop" + str(args.number) + ".csv")
    print("Top " + str(args.number) + " keywords saved to '" + top_N_output + "'.")
    top_N.to_csv(top_N_output, index=False)
except:
    print(traceback.format_exc())
