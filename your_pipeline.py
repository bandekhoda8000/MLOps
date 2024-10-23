from kfp import dsl
import kfp


def delete_pipeline_by_name(client:kfp.Client, pipeline_name: str):
    # List all pipelines
    pipelines = client.list_pipelines().pipelines

    # Find the pipeline with the given name
    for pipeline in pipelines:
        # print(f"Found pipeline: {pipeline.display_name} (ID: {pipeline.pipeline_id})")
        
        if pipeline.display_name == pipeline_name:
            # List versions of the pipeline
            versions = client.list_pipeline_versions(pipeline.pipeline_id).pipeline_versions
            
            # Delete all versions first
            for version in versions:
                print(version)
                print(f"Deleting pipeline version: {version.display_name} (ID: {version.pipeline_version_id})")
                client.delete_pipeline_version(pipeline.pipeline_id, version.pipeline_version_id)
            
            # Now delete the pipeline itself
            print(f"Deleting pipeline: {pipeline.display_name} (ID: {pipeline.pipeline_id})")
            client.delete_pipeline(pipeline.pipeline_id)
            return f"Pipeline {pipeline_name} and all its versions deleted successfully."

    return f"Pipeline {pipeline_name} not found."


@dsl.component(base_image='localhost:5000/pynuclio_base_3.8')
def hello_world_op():
    print('HEELOO WORLD!!')


@dsl.pipeline(
    name="Simple pipeline",
    description="A simple example of a Kubeflow pipeline"
)
def my_pipeline():
    hello_world_op()


if __name__ == "__main__":
    from kfp import compiler
    pipeline_file = 'simple_pipeline.yaml'
    name = 'test'
    compiler.Compiler().compile(my_pipeline, pipeline_file)
    client = kfp.Client()
    delete_pipeline_by_name(client, name)
    print('----------------- DELETED!!')
    client.pipeline_uploads.upload_pipeline(pipeline_file, name='test', )
    print('----------------- CREATED!!')
    for i in range(2):
        client.create_run_from_pipeline_func(my_pipeline, arguments={})
    print('----------------- RAN!!')
