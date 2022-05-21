/* tslint:disable */
/* eslint-disable */
/**
 * Lubricentro M&C
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0.0
 * Contact: matiasadrianpp4@gmail.com
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
/**
 * 
 * @export
 * @interface ProductUpdateCost
 */
export interface ProductUpdateCost {
    /**
     * 
     * @type {number}
     * @memberof ProductUpdateCost
     */
    porcentajeAumento?: number;
    /**
     * 
     * @type {Array<number>}
     * @memberof ProductUpdateCost
     */
    productos?: Array<number>;
}

export function ProductUpdateCostFromJSON(json: any): ProductUpdateCost {
    return ProductUpdateCostFromJSONTyped(json, false);
}

export function ProductUpdateCostFromJSONTyped(json: any, ignoreDiscriminator: boolean): ProductUpdateCost {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'porcentajeAumento': !exists(json, 'porcentaje_aumento') ? undefined : json['porcentaje_aumento'],
        'productos': !exists(json, 'productos') ? undefined : json['productos'],
    };
}

export function ProductUpdateCostToJSON(value?: ProductUpdateCost | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'porcentaje_aumento': value.porcentajeAumento,
        'productos': value.productos,
    };
}

