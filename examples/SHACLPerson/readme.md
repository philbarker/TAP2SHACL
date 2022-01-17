## SHACL Person Example
The example for a Person and employer used in the [W3C SHACL Recommendation](https://www.w3.org/TR/shacl/), cast as DC TAP.

* shaclPersonTAP.csv

Line 1: Person data may have zero or one `ex:ssn` property for Social Security Number, which must be a string matching the regulary expression for nnn-nn-nnnn (n = any digit)

Line 2: Person data may have zero or more `ex:worksFor` properties with an IRI referencing a node that matches the CompanyShape.

Line 3: Company data must have one and only one occurrence of the `rdf:type` property with the value `ex:Company` (or equivalent IRI).

* shaclPersonShapes.csv
Additional information about the shapes in the TAP, such as human readable labels and comments, but also:

Line 1: nodes of class `ex:Person` must match the PersonShape, which is closed, though any occurrence of rdf:type is ignored, any failure to match is a Violation of the application profile.

Line 2:  object nodes of the `ex:worksFor` property must match the CompanyShape, which is open, any failure to match is a Violation of the application profile.

* shacl.ttl : a SHACL file generated from this TAP.

* SampleData : valid and invalid sample data, also from the SHACL Recommendation, useful for testing validation artefacts (e.g. SHACL or ShEx files) generated from the TAP.
