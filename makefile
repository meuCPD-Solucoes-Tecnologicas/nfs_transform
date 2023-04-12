generate:
	python ./nfs_complementares.py NFS/Originais NFS/Complementares NFS/Base

generate_and_send:
	python  ./nfs_complementares.py --envio-producao NFS/Originais NFS/Complementares NFS/Base 2921 42596 

generate_and_homo:
	python  ./nfs_complementares.py --envio-homologacao NFS/Originais NFS/Complementares NFS/Base 2921 42596 

limpeza:
	rm -rf ./NFS/Complementares/*
	rm -rf ./NFS/Dicts_original/*
	rm -rf ./consultas/*
	rm -rf ./log/*.xml

limpeza-geral:
	rm -rf ./NFS/Complementares/*
	rm -rf ./NFS/Dicts_original/*
	rm -rf ./consultas/*
	rm -rf ./log/*
	