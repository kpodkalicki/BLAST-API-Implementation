# BLAST-API-Implementation

Library implementing API for Basic Local Alignment Search Tool <br/>
API specification: https://ncbi.github.io/blast-cloud/dev/api.html

## Requirements
- Python >= 3.6
- [requests](http://docs.python-requests.org/en/master/) 2.18.4

## How to use it
1. Create new instance of `BlastApiClient`
    ```python
   bc = BlastApiClient()
    ```
2. Launch a search using `BlastApiClien::search()` method
    ```python
    request_id, estimated_time = bc.search('u00001', 'nt', 'blastn')
    ```
3. `BlastApiClien::search()` method will return tuple of `(request_id, estimated_time)`.
    - `request_id` - can be used to retrieve results
    - `estimated_time`(RTOE) - estimated time in seconds until the search is completed
4. You can check the status of the search by using `BlastApiClien::check_submission_status()`
    ```python
    status = bc.check_submission_status(request_id)
    ```
    Method will return `status` as one of `WAITING`, `UNKNOWN`, or `READY`.
5. Once the search is finished, you may retrieve results by invoking `BlastApiClien::get_results()`
    ```python
    results = bc.get_results(request_id)
    ```
    `HTML` is default format of results
    
6. `BlastApiClien::wait_for_results()` can be used as a combination of `BlastApiClien::check_submission_status()` and 
`BlastApiClien::get_results()`. It'll wait until search is finished and retrieve results.
    ```python
    results = bc.wait_for_results(request_id, estimated_time=estimated_time)
    ```
    Note that `estimated_time` parameter is optional and doesn't need to be specified. Instead every 2 seconds method 
    will check search status and when it's `READY` retrieve results
    
## Avalilable parameters
- `BlastApiClien::search()`
    - **`query`** - Search query.
    - **`database`** - Name of existing database or one uploaded to blastdb_custom
    - **`program`** BLAST Program. One of: `['blastn', 'megablast', 'blastp', 'blastx', 'tblastn', 'tblastx']`
    - `filter` Low complexity filtering. `F` to disable. `T` or `L` to enable. Prepend “m” for mask at lookup (e.g., `mL`)
    - `format_type` - Report type. One of: `['HTML', 'Text', 'XML', 'XML2', 'JSON2', 'Tabular']`. Default: `'HTML'`.
    - `expect` - Expect value. Number greater than zero.
    - `nucl_reward` Reward for matching bases (BLASTN and megaBLAST). Integer greater than zero.
    - `gapcosts` Gap existence and extension costs. Tuple of two positive integers.
    - `matrix` Scoring matrix name. One of: `['BLOSUM45', 'BLOSUM50', 'BLOSUM62', 'BLOSUM80', 'BLOSUM90', 'PAM250',
                'PAM30' or 'PAM70']`. Default: `'BLOSUM62'`
    - `hitlist_size` - Number of databases sequences to keep. Integer greater than zero.
    - `descriptions` - Number of descriptions to print (applies to `HTML` and `Text`). Integer greater than zero.
    - `alignments` Number of alignments to print (applies to `HTML` and `Text`). Integer greater than zero.
    - `ncbi_gi` Show NCBI GIs in report. `'T'` or `'F'`
    - `threshold` - Neighboring score for initial words. Positive integer (BLASTP default is 11). Does not apply
                to BLASTN or MegaBLAST).
    - `word_size` - Size of word for initial matches. Positive integer.
    - `composition_based_statistics` - Composition based statistics algorithm to use. One of `[0, 1, 2, 3]`. See
                comp_based_stats in [BLAST+ user manual](https://www.ncbi.nlm.nih.gov/books/NBK279684/) for details.
    - `num_threads` - Number of virtual CPUs to use. 	Integer greater than zero (default is 1). *Supported only
            on the cloud*
            
- `BlastApiClien::check_submission_status()`
    - **`request_id`** - ID of requested search
    
- `BlastApiClien::get_results()`
    - **`request_id`** - ID of requested search
    - `format_type` - Report type. One of: `['HTML', 'Text', 'XML', 'XML2', 'JSON2', 'Tabular']`. Default: `'HTML'`.
    - `hitlist_size` - Number of databases sequences to keep. Integer greater than zero.
    - `descriptions` - Number of descriptions to print (applies to `HTML` and `Text`). Integer greater than zero.
    - `alignments` - Number of alignments to print (applies to `HTML` and `Text`). Integer greater than zero.
    - `ncbi_gi` - Show NCBI GIs in report. `'T'` or `'F'`
    - `format_object` - Object type. `SearchInfo` (status check) or `Alignment` (report formatting). Only `Alignment` is
                valid for retrieving results.
    - `results_file_path` - Results relative file path (applies to `XML2` and `JSON2`).

- `BlastApiClien::wait_for_results()`
    - The same as for `BlastApiClien::check_submission_status()` and `BlastApiClien::get_results()`

Parameters in **`bold`** are **required**.