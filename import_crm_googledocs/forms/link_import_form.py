from django import forms

from import_crm_googledocs.models.link_import_model import LinkImport


class LinkImportForm(forms.ModelForm):
    class Meta:
        model = LinkImport
        fields = ['link_google_docs']
        widgets = {
            'link_google_docs': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_link_google_docs(self):
        link_gdocs = self.cleaned_data.get('link_google_docs')

        if not link_gdocs.startswith("https://docs.google.com/spreadsheets") or \
                "/edit" not in link_gdocs:
            raise ValueError

        return link_gdocs
