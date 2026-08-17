import tarfile
import os
import sys

def extract_case_samples(sample_per_year=50000):
    os.makedirs('data/extracted/cases_sample', exist_ok=True)
    raw_path = 'data/raw/cases.tar.gz'
    print(f"Streaming from {raw_path}...")
    
    with tarfile.open(raw_path, 'r:gz') as tar:
        for member in tar:
            if not member.isfile() or not member.name.endswith('.csv'):
                continue
            fname = os.path.basename(member.name)
            out_path = os.path.join('data/extracted/cases_sample', f"sample_{fname}")
            print(f"Sampling {sample_per_year} rows from {fname} -> {out_path}...", flush=True)
            
            f = tar.extractfile(member)
            with open(out_path, 'w', encoding='utf-8', errors='replace') as out_f:
                # Read header
                header = f.readline().decode('utf-8', errors='replace')
                out_f.write(header)
                count = 0
                for line in f:
                    out_f.write(line.decode('utf-8', errors='replace'))
                    count += 1
                    if count >= sample_per_year:
                        break
            print(f"  Extracted {count} rows for {fname}", flush=True)

def extract_acts_sample(sample_rows=500000):
    raw_path = 'data/raw/acts_sections.tar.gz'
    out_path = 'data/extracted/acts_sections_sample.csv'
    print(f"Streaming from {raw_path} to {out_path}...", flush=True)
    
    with tarfile.open(raw_path, 'r:gz') as tar:
        for member in tar:
            if not member.isfile() or not member.name.endswith('.csv'):
                continue
            f = tar.extractfile(member)
            with open(out_path, 'w', encoding='utf-8', errors='replace') as out_f:
                header = f.readline().decode('utf-8', errors='replace')
                out_f.write(header)
                count = 0
                for line in f:
                    out_f.write(line.decode('utf-8', errors='replace'))
                    count += 1
                    if count >= sample_rows:
                        break
            print(f"  Extracted {count} rows for acts_sections", flush=True)
            break

if __name__ == '__main__':
    extract_case_samples(sample_per_year=50000)
    extract_acts_sample(sample_rows=500000)
