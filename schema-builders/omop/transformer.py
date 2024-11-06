import random
from linkml_runtime.linkml_model import SlotDefinition
from linkml.validator import validate
from linkml_map.session import Session
from linkml.utils.schema_builder import SchemaBuilder

import sys
import yaml
from datetime import datetime


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

maleConceptId = random.randint(1, 1000)
femaleConceptId = maleConceptId + 1

print(maleConceptId)
print(femaleConceptId)

person_occurence_session = Session()
person_occurence_session.set_source_schema(sb.as_dict())
person_occurence_session.set_object_transformer(f"""
  class_derivations:
    Person_occurence:
      populated_from: LinkMLModel
      slot_derivations:
        person_id:
          expr: {random.randint(1, 1000)}
        year_of_birth:
          expr: {datetime.now().year} - {{age}}
        gender_concept_id:
          expr: {maleConceptId} if {{sex}} == 'Male' else {femaleConceptId}
        condition_source_value:
          populated_from: disease
  """)

person_occurence_sb = SchemaBuilder()
for person_occurence_class in person_occurence_session.target_schema.classes:
  person_occurence_sb.add_class(
    person_occurence_class,
  )
person_occurence_sb.add_defaults()

print(person_occurence_sb.as_dict())

person_session = Session()
person_session.set_source_schema(sb.as_dict())
person_session.set_object_transformer(f"""
  class_derivations:
    Person:
      populated_from: Person_occurence
      slot_derivations:
        person_id:
          expr: {random.randint(1, 1000)}
        year_of_birth:
          expr: {datetime.now().year} - {{age}}
        gender_concept_id:
          expr: {maleConceptId} if {{sex}} == 'Male' else {femaleConceptId}
  """)

condition_occurence_session = Session()
condition_occurence_session.set_source_schema(person_occurence_session)
condition_occurence_session.set_object_transformer(f"""
  class_derivations:
    Condition_occurrence:
      populated_from: Person_occurence
      joins:
        alias: Person
        class_named: Person
      slot_derivations:
        condition_occurrence_id:
          expr: {random.randint(1, 1000)}
        condition_source_value:
          populated_from: disease
        person_id:
          expr: person_id
  """)
obj = {
  "sex": "Male",
  "age": 42,
  "disease": "Lymphoma",
}

report = validate(obj, sb.as_dict(), 'LinkMLModel')
for r in report.results:
  if r.severity == 'ERROR':
    sys.exit(1)

person_occurence = person_occurence_session.transform(obj)
print(person_session.transform(obj))
# print(condition_occurence_session.transform(person_occurence))
