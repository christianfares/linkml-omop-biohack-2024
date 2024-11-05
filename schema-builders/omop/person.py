from linkml.utils.schema_builder import SchemaBuilder
from linkml_runtime.linkml_model import SlotDefinition

sb = SchemaBuilder()
sb.add_class("Person", slots=[SlotDefinition("family_name", range="string"), 
                              SlotDefinition("given_name", range="string"),
                              SlotDefinition("age_in_years", range="integer"),
                              SlotDefinition("height_in_cm", range="float"),
                              ])
sb.add_defaults()
print(yaml.dump(sb.as_dict(), sort_keys=False))
