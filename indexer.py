from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchIndex, SimpleField, SearchFieldDataType, SearchableField, VectorField,
    SearchIndexerDataSourceConnection, SearchIndexerDataContainer,
    SearchIndexerSkillset, SplitSkill, InputFieldMappingEntry, OutputFieldMappingEntry,
    SearchIndexer, FieldMapping, CognitiveServicesAccountKey,KeyPhraseExtractionSkill,
    EntityLinkingSkill,
)
from azure.core.credentials import AzureKeyCredential
import os

search_service_name = os.environ.get('AZURE_SEARCH_SERVICE_NAME')
search_service_admin_key = os.environ.get('SEARCH_SERVICE_ADMIN_KEY')
cognitive_services_key = os.environ.get('COGNITIVE_SERVICES_KEY')
data_source_connection_string = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
container_name = os.environ.get('CONTAINER_NAME')
index_name =os.environ.get('INDEX_NAME')
search_indexer_name = os.environ.get('SEARCH_INDEXER_NAME')
data_sorurce_name = os.environ.get('DATA_SOURCE_NAME')

endpoint = f'https://{search_service_name}.search.windows.net'

credential = AzureKeyCredential(search_service_admin_key)

index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
indexer_client = SearchIndexerClient(endpoint=endpoint, credential=credential)

fields = [
    SimpleField(name='id', type=SearchFieldDataType.String, key=True),
    SearchableField(
        name='chunks',
        type=SearchFieldDataType.String,
        collection=True,
        searchable=True,
        analyzer_name='en.lucene'
    ),
    SimpleField(name='metadata_storage_path',
                type=SearchFieldDataType.String, filterable=True),
]

fields = [
    SimpleField(name='id', type=SearchFieldDataType.String, key=True),

    # The chunked content
    SearchableField(name='chunks', type=SearchFieldDataType.String,
                    searchable=True, analyzer_name='en.lucene'),

    SimpleField(name='metadata_storage_path',
                type=SearchFieldDataType.String, filterable=True),

    SearchableField(
        name='keyPhrases',
        type=SearchFieldDataType.String,
        collection=True,
        searchable=True,
    ),
    SearchableField(
        name='entities',
        type=SearchFieldDataType.String,
        collection=True,
        searchable=True,
        facetable=True,

    ),

    SearchableField(name='title', type=SearchFieldDataType.String,
                    searchable=True, filterable=True, sortable=True),
    SimpleField(name='published_date', type=SearchFieldDataType.DateTimeOffset,
                filterable=True, sortable=True, facetable=True),
    SimpleField(name='content_length', type=SearchFieldDataType.Int32,
                filterable=True, facetable=True, sortable=True),
]
index = SearchIndex(name=index_name, fields=fields)

try:
    index_client.create_or_update_index(index)
    print(f"Index '{index_name}' created or updated successfully.")
except Exception as e:
    print(f"Error creating or updating index: {e}")



data_source = SearchIndexerDataSourceConnection(
    name='fitness-data-source-connection',
    type="azureblob",
    connection_string=data_source_connection_string,
    container=SearchIndexerDataContainer(name=container_name)
)

try:
    indexer_client.create_or_update_data_source_connection(data_source)
    print("Data source created or updated successfully.")
except Exception as e:
    print(f"Error creating or updating data source: {e}")


# Initialize the skillset with additional skills
skillset = SearchIndexerSkillset(
    name='fitness-skillset',
    description="Skillset including chunking and metadata extraction",
    skills=[
        SplitSkill(
            name="SplitSkill",
            description="Split content into chunks",
            context="/document",
            text_split_mode="sentences",
            maximum_page_length=1000,
            default_language_code="en",
            inputs=[
                InputFieldMappingEntry(name="text", source="/document/content")
            ],
            outputs=[
                OutputFieldMappingEntry(name="textItems", target_name="chunks")
            ]
        ),
        KeyPhraseExtractionSkill(
            name="KeyPhraseExtractionSkill",
            context="/document/chunks/*",
            description="Extract key phrases from each chunk",
            default_language_code="en",
            inputs=[
                InputFieldMappingEntry(
                    name="text", source="/document/chunks/*")
            ],
            outputs=[
                OutputFieldMappingEntry(
                    name="keyPhrases", target_name="keyPhrases")
            ]
        ),

        EntityLinkingSkill(
            name="EntityRecognitionSkill",
            context="/document/chunks/*",
            description="Recognize entities in each chunk",
            default_language_code="en",
            inputs=[
                InputFieldMappingEntry(
                    name="text", source="/document/chunks/*")
            ],
            outputs=[
                OutputFieldMappingEntry(
                    name="entities", target_name="entities")
            ]
        ),
    ],
    cognitive_services_account=CognitiveServicesAccountKey(
        description="Cognitive Services Key",
        key=cognitive_services_key
    )
)


try:
    indexer_client.create_or_update_skillset(skillset)
    print("Skillset with chunking created or updated successfully.")
except Exception as e:
    print(f"Error creating or updating skillset: {e}")

# Create Indexer with Field Mappings
indexer = SearchIndexer(
    name='fitness-indexer',
    data_source_name=data_source.name,
    target_index_name=index.name,
    skillset_name=skillset.name,
    field_mappings=[
        FieldMapping(
            source_field_name='metadata_storage_path',
            target_field_name='metadata_storage_path'
        )
    ],
    output_field_mappings=[
        FieldMapping(
            source_field_name='/document/chunks/*',
            target_field_name='chunks'
        )
    ]
)

indexer = SearchIndexer(
    name='pdf-indexer',
    data_source_name=data_source.name,
    target_index_name=index.name,
    skillset_name=skillset.name,
    field_mappings=[],
    output_field_mappings=[
        FieldMapping(

            source_field_name='/document/chunks/*',
            target_field_name='chunks'
        ),
        FieldMapping(
            source_field_name='/document/chunks/*/keyPhrases',
            target_field_name='keyPhrases'
        ),

        FieldMapping(
            source_field_name='/document/chunks/*/entities/*/text',
            target_field_name='entities'
        ),
        FieldMapping(
            source_field_name='/document/metadata_storage_name',
            target_field_name='title'
        ),
        FieldMapping(
            source_field_name='/document/metadata_storage_last_modified',
            target_field_name='published_date'
        ),
        FieldMapping(
            source_field_name='/document/metadata_storage_size',
            target_field_name='content_length'
        ),
        FieldMapping(
            source_field_name='/document/metadata_storage_path',
            target_field_name='metadata_storage_path'
        ),
    ]
)

try:
    indexer_client.create_or_update_indexer(indexer)
    indexer_client.run_indexer(indexer.name)
    print("Indexer with chunking is running.")
except Exception as e:
    print(f"Error running indexer: {e}")
