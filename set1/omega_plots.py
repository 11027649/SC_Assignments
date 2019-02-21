import pandas as pd

def main():
    df = pd.read_csv('omega_results.csv', sep=',')
    print(df)
    
if __name__ == '__main__':
    main()
