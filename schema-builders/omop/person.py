import random
from linkml_runtime.linkml_model import SlotDefinition
from linkml.validator import validate
from linkml_map.session import Session
from linkml.utils.schema_builder import SchemaBuilder

import sys
import yaml

sb = SchemaBuilder()
sb.add_enum('GenderEnum', ['Male', 'Female'])
sb.add_class(
  "LinkMLModel",
  slots=[
    SlotDefinition("age", range="integer"), 
    SlotDefinition("sex", range="GenderEnum"),
    SlotDefinition("disease", range="string"),
  ],
)
sb.add_defaults()
print(yaml.dump(sb.as_dict(), sort_keys=False))

maleConceptId = random.randint(1, 1000)
femaleConceptId = maleConceptId + 1

print(maleConceptId)
print(femaleConceptId)

session = Session()
session.set_source_schema(sb.as_dict())
session.set_object_transformer(f"""
class_derivations:
  DiseaseConcept:
    populated_from: LinkMLModel
    slot_derivations:
      concept_id:
        expr: {random.randint(1, 1000)}
      concept_name:
        populated_from: disease
      domain_id: 
        expr: "'Condition'"
      vocabulary_id:
        expr: "'Condition'"
      concept_class_id:
        expr: "'Condition'"
""")
# session.set_object_transformer(f"""
# class_derivations:
#   GenderConcept:
#     populated_from: LinkMLModel
#     slot_derivations:
#       concept_id:
#         expr: {maleConceptId} if {{sex}} == 'Male' else {femaleConceptId}
#       concept_name:
#         populated_from: sex
#       domain_id: 
#         expr: "'Gender'"
#       vocabulary_id:
#         expr: "'Gender'"
#       concept_class_id:
#         expr: "'Gender'"
#   DiseaseConcept:
#     populated_from: LinkMLModel
#     slot_derivations:
#       concept_id:
#         expr: {random.randint(1, 1000)}
#       concept_name:
#         populated_from: disease
#       domain_id: 
#         expr: "'Condition'"
#       vocabulary_id:
#         expr: "'Condition'"
#       concept_class_id:
#         expr: "'Condition'"
# """)

obj = {
  "sex": "Male",
  "age": 42,
  "disease": "Lymphoma",
}

report = validate(obj, 'models/omop/concept.yml', 'Concept')
print(report)
for r in report.results:
  if r.severity == 'ERROR':
    sys.exit(1)

print(session.transform(obj))
