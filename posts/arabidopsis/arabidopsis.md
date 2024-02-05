---
title: "Analyzing Gene Functions in Arabidopsis Thaliana"
date: 03 February 2024
---

[The Arabidopsis Information Resource (TAIR)](https://www.arabidopsis.org/) maintains a database of genetic and molecular biology data for the model higher plant Arabidopsis thaliana. We can do all sorts of analyses with this data, but in this post we will focus on looking at gene functions. You can download the annotation data (ATH_GO_GOSLIM.txt.gz) from the TAIR site, but I also included it in my Github repo [mlg556/arabidopsis](https://github.com/mlg556/arabidopsis), so you can just clone that.

First let's import the libraries. We will use [pandas](https://pandas.pydata.org/) for reading/analyzing the data, and `zipfile` to extract the data file, which is archived. You can simply install pandas via `pip install pandas`, and `zipfile` is a built-in python library.


```python
import pandas as pd
import zipfile
```

We extract the archived file `ATH_GO_GOSLIM.txt.gz` to `ATH_GO_GOSLIM.txt`. Note that although the extension `.gz` suggests Gzip/7zip file, we need a regular zip extractor.


```python
# extract txt, file extension is erroneously gz, but its actually a zip file
fname = "ATH_GO_GOSLIM.txt"
fname_gz = f"{fname}.gz"

with zipfile.ZipFile(fname_gz, 'r') as z:
    z.extractall(".")
```

The resulting file is txt file using '\t' as a delimiter. The column header names is absent, but we can read that from the companion file `ATH_GO.README.txt`, which I also included in the repo. To read the data into a pandas dataframe, I used `read_csv`. We specify the separator with `sep="\t"`, and the column names. We need skip the first 4 rows because they are comments:

```
!Project_name: The Arabidopsis Information Resource (TAIR)
!URL: http://www.arabidopsis.org
!Contact Email: curator@arabidopsis.org
!Last Updated: 2023-12-01
```

Finally we print the dataframe see what it looks like


```python
# column data from from ATH_GO.README.txt
columns = [
    "locus_name",
    "tair_acc",
    "obj_name",
    "rel_type",
    "go_term",
    "go_id",
    "tair_id",
    "aspect",
    "go_slim",
    "evidence_code",
    "evidence_desc",
    "evidence_with",
    "reference",
    "annotator",
    "date"
]


# read into dataframe
df0 = pd.read_csv(fname, sep="\t", names=columns, skiprows=[0,1,2,3])
df0
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>locus_name</th>
      <th>tair_acc</th>
      <th>obj_name</th>
      <th>rel_type</th>
      <th>go_term</th>
      <th>go_id</th>
      <th>tair_id</th>
      <th>aspect</th>
      <th>go_slim</th>
      <th>evidence_code</th>
      <th>evidence_desc</th>
      <th>evidence_with</th>
      <th>reference</th>
      <th>annotator</th>
      <th>date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AT1G01010</td>
      <td>locus:2200935</td>
      <td>AT1G01010</td>
      <td>acts upstream of or within</td>
      <td>defense response to other organism</td>
      <td>GO:0098542</td>
      <td>46569</td>
      <td>P</td>
      <td>response to stress</td>
      <td>IEA</td>
      <td>traceable computational prediction</td>
      <td>AGI_LocusCode:AT2G43510|AGI_LocusCode:AT4G1473...</td>
      <td>Publication:501796011|PMID:34562334</td>
      <td>klaasvdp</td>
      <td>2022-11-14</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AT1G01010</td>
      <td>locus:2200935</td>
      <td>AT1G01010</td>
      <td>acts upstream of or within</td>
      <td>response to oxidative stress</td>
      <td>GO:0006979</td>
      <td>6625</td>
      <td>P</td>
      <td>response to stress</td>
      <td>IEA</td>
      <td>traceable computational prediction</td>
      <td>AGI_LocusCode:AT5G19875</td>
      <td>Publication:501796011|PMID:34562334</td>
      <td>klaasvdp</td>
      <td>2022-11-14</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AT1G01010</td>
      <td>locus:2200935</td>
      <td>AT1G01010</td>
      <td>acts upstream of or within</td>
      <td>response to abscisic acid</td>
      <td>GO:0009737</td>
      <td>11395</td>
      <td>P</td>
      <td>response to chemical</td>
      <td>IEA</td>
      <td>traceable computational prediction</td>
      <td>AGI_LocusCode:AT4G27410</td>
      <td>Publication:501796011|PMID:34562334</td>
      <td>klaasvdp</td>
      <td>2022-11-14</td>
    </tr>
    <tr>
      <th>3</th>
      <td>AT1G01010</td>
      <td>locus:2200935</td>
      <td>AT1G01010</td>
      <td>acts upstream of or within</td>
      <td>response to lipid</td>
      <td>GO:0033993</td>
      <td>28865</td>
      <td>P</td>
      <td>response to chemical</td>
      <td>IEA</td>
      <td>traceable computational prediction</td>
      <td>AGI_LocusCode:AT4G27410|AGI_LocusCode:AT2G0299...</td>
      <td>Publication:501796011|PMID:34562334</td>
      <td>klaasvdp</td>
      <td>2022-11-14</td>
    </tr>
    <tr>
      <th>4</th>
      <td>AT1G01010</td>
      <td>locus:2200935</td>
      <td>AT1G01010</td>
      <td>acts upstream of or within</td>
      <td>oxoacid metabolic process</td>
      <td>GO:0043436</td>
      <td>21524</td>
      <td>P</td>
      <td>other cellular processes</td>
      <td>IEA</td>
      <td>traceable computational prediction</td>
      <td>AGI_LocusCode:AT5G63790</td>
      <td>Publication:501796011|PMID:34562334</td>
      <td>klaasvdp</td>
      <td>2022-11-14</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>456201</th>
      <td>YAK</td>
      <td>gene:1945468</td>
      <td>YAK</td>
      <td>is active in</td>
      <td>cellular_component</td>
      <td>GO:0005575</td>
      <td>163</td>
      <td>C</td>
      <td>unknown cellular components</td>
      <td>ND</td>
      <td>'Unknown' cellular component</td>
      <td>NONE</td>
      <td>Communication:1345790</td>
      <td>TAIR</td>
      <td>2022-02-01</td>
    </tr>
    <tr>
      <th>456202</th>
      <td>YAK</td>
      <td>gene:1945468</td>
      <td>YAK</td>
      <td>enables</td>
      <td>molecular_function</td>
      <td>GO:0003674</td>
      <td>3226</td>
      <td>F</td>
      <td>unknown molecular functions</td>
      <td>ND</td>
      <td>'Unknown' molecular function</td>
      <td>NaN</td>
      <td>Communication:1345790</td>
      <td>TAIR</td>
      <td>2006-10-20</td>
    </tr>
    <tr>
      <th>456203</th>
      <td>YI</td>
      <td>gene:1945470</td>
      <td>YI</td>
      <td>involved in</td>
      <td>biological_process</td>
      <td>GO:0008150</td>
      <td>5239</td>
      <td>P</td>
      <td>unknown biological processes</td>
      <td>ND</td>
      <td>'Unknown' biological process</td>
      <td>NONE</td>
      <td>Communication:1345790</td>
      <td>TAIR</td>
      <td>2022-02-01</td>
    </tr>
    <tr>
      <th>456204</th>
      <td>YI</td>
      <td>gene:1945470</td>
      <td>YI</td>
      <td>is active in</td>
      <td>cellular_component</td>
      <td>GO:0005575</td>
      <td>163</td>
      <td>C</td>
      <td>unknown cellular components</td>
      <td>ND</td>
      <td>'Unknown' cellular component</td>
      <td>NONE</td>
      <td>Communication:1345790</td>
      <td>TAIR</td>
      <td>2022-02-01</td>
    </tr>
    <tr>
      <th>456205</th>
      <td>YI</td>
      <td>gene:1945470</td>
      <td>YI</td>
      <td>enables</td>
      <td>molecular_function</td>
      <td>GO:0003674</td>
      <td>3226</td>
      <td>F</td>
      <td>unknown molecular functions</td>
      <td>ND</td>
      <td>'Unknown' molecular function</td>
      <td>NaN</td>
      <td>Communication:1345790</td>
      <td>TAIR</td>
      <td>2006-10-20</td>
    </tr>
  </tbody>
</table>
<p>456206 rows × 15 columns</p>
</div>



As you can see, this is a quite large dataframe with $456\,206$ genes and their associated functions. The `go_term` column is a nice description of what the gene does, so we will use that. I have also noticed that there are 3 GO terms we need to exclude, because they are very generic and not useful: `["molecular_function", "biological_process", "cellular_component"]`.

We select the columns by indexing into the dataframe, drop duplicates, and finally drop the rows which contain the excluded go_terms with `query()`. We could also use indexing for this, but query looks nicer I think.


```python
select_columns = ["locus_name", "go_term"]

excluded_go_terms = ["molecular_function", "biological_process", "cellular_component"]

df = df0[select_columns] # select gene name and function
df = df.drop_duplicates() # drop duplicates
df = df.query("go_term not in @excluded_go_terms") # exclude go_terms

df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>locus_name</th>
      <th>go_term</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AT1G01010</td>
      <td>defense response to other organism</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AT1G01010</td>
      <td>response to oxidative stress</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AT1G01010</td>
      <td>response to abscisic acid</td>
    </tr>
    <tr>
      <th>3</th>
      <td>AT1G01010</td>
      <td>response to lipid</td>
    </tr>
    <tr>
      <th>4</th>
      <td>AT1G01010</td>
      <td>oxoacid metabolic process</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>456175</th>
      <td>XRS9</td>
      <td>DNA damage response</td>
    </tr>
    <tr>
      <th>456176</th>
      <td>XRS9</td>
      <td>DNA repair</td>
    </tr>
    <tr>
      <th>456182</th>
      <td>XRS9</td>
      <td>response to X-ray</td>
    </tr>
    <tr>
      <th>456183</th>
      <td>XTC1</td>
      <td>embryo development ending in seed dormancy</td>
    </tr>
    <tr>
      <th>456190</th>
      <td>XTC2</td>
      <td>embryo development ending in seed dormancy</td>
    </tr>
  </tbody>
</table>
<p>175917 rows × 2 columns</p>
</div>



We are left with a table $175\,917$  of genes with their corresponding functions, but I want to analyze them by function. Let's see which functions are done by which genes. We do this by using `groupby`:


```python
dfg = df.groupby("go_term", as_index=False).apply(lambda x: x)
dfg
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>locus_name</th>
      <th>go_term</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="3" valign="top">0</th>
      <th>59240</th>
      <td>AT1G36280</td>
      <td>'de novo' AMP biosynthetic process</td>
    </tr>
    <tr>
      <th>264420</th>
      <td>AT3G57610</td>
      <td>'de novo' AMP biosynthetic process</td>
    </tr>
    <tr>
      <th>301471</th>
      <td>AT4G18440</td>
      <td>'de novo' AMP biosynthetic process</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">1</th>
      <th>52413</th>
      <td>AT1G30820</td>
      <td>'de novo' CTP biosynthetic process</td>
    </tr>
    <tr>
      <th>161072</th>
      <td>AT2G34890</td>
      <td>'de novo' CTP biosynthetic process</td>
    </tr>
    <tr>
      <th>...</th>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">7460</th>
      <th>97088</th>
      <td>AT1G69770</td>
      <td>zygote asymmetric cytokinesis in embryo sac</td>
    </tr>
    <tr>
      <th>118068</th>
      <td>AT2G01210</td>
      <td>zygote asymmetric cytokinesis in embryo sac</td>
    </tr>
    <tr>
      <th>412150</th>
      <td>AT5G49160</td>
      <td>zygote asymmetric cytokinesis in embryo sac</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">7461</th>
      <th>129874</th>
      <td>AT2G17090</td>
      <td>zygote elongation</td>
    </tr>
    <tr>
      <th>157944</th>
      <td>AT2G33160</td>
      <td>zygote elongation</td>
    </tr>
  </tbody>
</table>
<p>175917 rows × 2 columns</p>
</div>



We see that, for example *'de novo' AMP biosynthetic process* is regulated by three different genes: AT1G36280, AT3G57610 and AT4G18440. We can see which functions are regulated by the most number of genes using grouby combined with count, and sort them in descending order:


```python
dfg_sum = df.groupby("go_term").count()
dfg_sum = dfg_sum.sort_values(by=['locus_name'], ascending=False)
dfg_sum
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>locus_name</th>
    </tr>
    <tr>
      <th>go_term</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>nucleus</th>
      <td>10494</td>
    </tr>
    <tr>
      <th>chloroplast</th>
      <td>4966</td>
    </tr>
    <tr>
      <th>cytoplasm</th>
      <td>4771</td>
    </tr>
    <tr>
      <th>protein binding</th>
      <td>4519</td>
    </tr>
    <tr>
      <th>mitochondrion</th>
      <td>4449</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
    </tr>
    <tr>
      <th>organelle fission</th>
      <td>1</td>
    </tr>
    <tr>
      <th>beta,beta digalactosyldiacylglycerol galactosyltransferase activity</th>
      <td>1</td>
    </tr>
    <tr>
      <th>regulation of MAPK cascade</th>
      <td>1</td>
    </tr>
    <tr>
      <th>regulation of GTPase activity</th>
      <td>1</td>
    </tr>
    <tr>
      <th>regulation of trichome patterning</th>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>7462 rows × 1 columns</p>
</div>



This is nice, but not very helpful. Go terms like *nucleus* and *protein binding* seem to me too broad to be meaningful. Of course at the other end we have very specific functions regulated by a single gene. I would like to see more of what's in between, so let's look at the distribution:


```python
import matplotlib.pyplot as plt
distribution = dfg_sum.iloc[:50].plot.bar(figsize=(20, 5))

```
    
![Gene function distribution.](arabidopsis_files/arabidopsis_17_0.png)
    

Apart from the usual suspects, the more interesting functions to me are "response to water deprivation", "response to light stimulus" and "response to abscisic acid". We see that the type of things which are more important to a plant have more genes to express/regulate them. Abscisic acid is a *plant hormone that regulates numerous aspects of plant growth, development, and stress responses.*

Another thing worthy of notice is that the distribution seems to follow a [*power law*](https://en.wikipedia.org/wiki/Power_law) and the [*Pareto principle*](https://en.wikipedia.org/wiki/Pareto_principle). I don't know if this is to be expected or not.


```python
plot = dfg_sum.iloc[:100].plot(figsize=(20, 5), marker=".", grid=True)
plot.plot([10_000/x for x in range(1,100)])
_ = plot.legend(["locus_name", "1/x"])
```


    
![Power law.](arabidopsis_files/arabidopsis_20_0.png)
    


# Citations

* Berardini, TZ, Mundodi, S, Reiser, R, Huala, E, Garcia-Hernandez, M, Zhang, P, Mueller, LM, Yoon, J, Doyle, A, Lander, G, Moseyko, N, Yoo, D, Xu, I, Zoeckler, B, Montoya, M, Miller, N, Weems, D, and Rhee, SY (2004) Functional annotation of the Arabidopsis genome using controlled vocabularies. Plant Physiol. 135(2):1-11.

* TAIR Terms of Use: http://www.arabidopsis.org/doc/about/tair_terms_of_use/417.
