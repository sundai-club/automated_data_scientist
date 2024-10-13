from flask import Flask, request, jsonify
import pandas as pd
# import pyvcf  # PyVCF for reading VCF files
import allel  # scikit-allel for VCF parsing
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)

@app.route('/vcf-analysis', methods=['POST'])
def vcf_analysis():
    """
    Analyzes a VCF (Variant Call Format) file and generates a 2D PCA plot along with
    the code and description used to create the plot.

    Input:
    ------
    Request Type: POST
    - VCF File: Multipart file upload containing genomic data (.vcf).
    - Prompt: string
        A user input prompt to guide the type of analysis and plot generation.

    Output:
    -------
    JSON Response:
    - plot_image: string (Base64 encoded image of the generated 2D plot).
    - code: string
        Code snippet used to generate the plot.
    - description: string
        Brief description of the generated plot and code logic.
    """
    try:
        # 1. Validate inputs: Ensure VCF file and prompt are included
        if 'vcf_file' not in request.files or 'prompt' not in request.form:
            return jsonify({"error": "Missing VCF file or prompt"}), 400

        # 2. Extract VCF file and prompt from request
        vcf_file = request.files['vcf_file']
        prompt = request.form['prompt']

        # 3. Ensure the uploaded file is a valid VCF file
        if not vcf_file.filename.endswith('.vcf'):
            return jsonify({"error": "Uploaded file is not a .vcf file"}), 400

        # 4. Parse VCF file and extract genotype data
        # vcf_reader = vcf.Reader(vcf_file.stream)
        # genotype_data = extract_genotype_data(vcf_reader)

        # 5. Perform PCA to reduce dimensionality to 2D
        # pca_result = perform_pca(genotype_data)

        # 6. Generate the 2D PCA plot and encode it in Base64
        # plot_image = generate_plot(pca_result)

        # 7. Provide a code snippet and brief description
        code_snippet = """
import matplotlib.pyplot as plt
plt.scatter(pca_result[:, 0], pca_result[:, 1])
plt.title('2D PCA of Genomic Data')
plt.show()
        """
        description = f"Generated a PCA plot from {len(genotype_data)} genomic samples using the first two principal components."

        # 8. Return JSON response with plot, code, and description
        return jsonify({
            "plot_image": plot_image,
            "code": code_snippet,
            "description": description
        }), 200

    except Exception as e:
        # Handle any errors that occur during processing
        return jsonify({"error": str(e)}), 500

def extract_genotype_data(vcf_reader):
    """
    Extracts genotype data from the VCF reader object.
    """
    genotypes = []
    for record in vcf_reader:
        sample_genotypes = [call.gt_type for call in record.samples]  # 0 = homozygous ref, 1 = heterozygous, 2 = homozygous alt
        genotypes.append(sample_genotypes)
    return pd.DataFrame(genotypes)

def perform_pca(genotype_data):
    """
    Performs PCA on the genotype data.
    """
    # Replace NaN with 0 for PCA analysis
    genotype_data = genotype_data.fillna(0)

    # Apply PCA to reduce to 2 components
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(genotype_data)

    return pca_result

def generate_plot(pca_result):
    """
    Generates a 2D scatter plot from the PCA results and encodes it as a Base64 image.
    """
    plt.figure(figsize=(8, 6))
    plt.scatter(pca_result[:, 0], pca_result[:, 1], alpha=0.7)
    plt.title("2D PCA of Genomic Data")
    plt.xlabel("PC1")
    plt.ylabel("PC2")

    # Save plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode plot as Base64 string
    plot_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    return plot_base64

if __name__ == '__main__':
    app.run(debug=True)
